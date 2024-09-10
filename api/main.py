import os
from dotenv import load_dotenv

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
# from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache

from typing import Union, Optional, Type
from utils.student import Student
from utils.instructor import Instructor
from utils.course import Course
from utils.enrollment import Enrollment

from utils.logging import logging

from sqlmodel import SQLModel, select
from sqlmodel.sql.expression import SelectOfScalar
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Engine

from typing import Dict


from config import (
    # ONE_DAY_SEC,
    ONE_WEEK_SEC,
    ENV_PATH,
    USE_REDIS_CACHE,
    USE_POSTGRES_DB,
    DESCRIPTION,
)

load_dotenv(ENV_PATH)

sms_resource: Dict[str,
                   Union[Engine, logging.Logger]] = {}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Cache
    if USE_REDIS_CACHE:
        from redis import asyncio as aioredis
        from fastapi_cache.backends.redis import RedisBackend
        url = os.getenv("REDIS_URL")
        username = os.getenv("REDIS_USERNAME")
        password = os.getenv("REDIS_PASSWORD")
        redis = aioredis.from_url(url=url, username=username,
                                  password=password, encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    else:
        # In Memory cache
        FastAPICache.init(InMemoryBackend())

    # Database
    if USE_POSTGRES_DB:
        DATABASE_URL = os.getenv("POSTGRES_URL")
        connect_args = {
            "timeout": 60
        }
    else:  # sqlite
        DATABASE_URL = "sqlite+aiosqlite:///sms.db"
        # Allow a single connection to be accessed from multiple threads.
        connect_args = {"check_same_thread": False}

    # Define the async engine
    engine = create_async_engine(
        DATABASE_URL, echo=True, connect_args=connect_args)

    sms_resource["engine"] = engine

    # Startup actions: create database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Logger
    logger = logging.getLogger(__name__)

    sms_resource["logger"] = logger

    yield  # Application code runs here

    # Shutdown actions: close connections, etc.
    await engine.dispose()


# FastAPI Object
app = FastAPI(
    title='School Management System API',
    version='1.0.0',
    description=DESCRIPTION,
    lifespan=lifespan,
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get('/favicon.ico', include_in_schema=False)
@cache(expire=ONE_WEEK_SEC, namespace='eta_favicon')  # Cache for 1 week
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "assets", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


# API

OneResult = Union[Student, Instructor, Course, Enrollment]
OneResultItem = Optional[OneResult]

BulkResult = Dict[str, OneResult]
BulkResultItem = Optional[BulkResult]

Result = Union[OneResult, BulkResult]
ResultItem = Union[OneResultItem, BulkResultItem]


class EndpointResponse(SQLModel):
    execution_msg: str
    execution_code: int
    result: ResultItem


class ErrorResponse(SQLModel):
    execution_msg: str
    execution_code: int
    error: Optional[str]


# Endpoints

# Status endpoint: check if api is online
@app.get('/', tags=['Home'])
async def status_check():
    return {"Status": "API is online..."}


async def endpoint_output(endpoint_result: Result, code: int = 0, error: str = None) -> Union[ErrorResponse, EndpointResponse]:
    msg = 'Execution failed'
    output = ErrorResponse(**{'execution_msg': msg,
                              'execution_code': code, 'error': error})

    try:
        if code != 0:
            msg = 'Execution was successful'
            output = EndpointResponse(
                **{'execution_msg': msg,
                   'execution_code': code, 'result': endpoint_result}
            )

    except Exception as e:
        code = 0
        msg = 'Execution failed'
        errors = f"Omg, an error occurred. endpoint_output Error: {e} & endpoint_result Error: {error} & endpoint_result: {endpoint_result}"
        output = ErrorResponse(**{'execution_msg': msg,
                                  'execution_code': code, 'error': errors})

        sms_resource["logger"].error(error)

    finally:
        return output


# Caching Post requests is challenging
async def sms_posts(instance: Result, idx: str = None, action: str = "add") -> Union[ErrorResponse, EndpointResponse]:
    async with AsyncSession(sms_resource["engine"]) as session:
        code = 0
        error = None
        existing = await session.get(instance.__class__, idx)

        # For add action, do db operation if instance is not existing. Other actions, do db operation if instance exists in db
        checker = existing is None if action == "add" else existing is not None

        try:
            if checker:
                if action == "delete":
                    session.delete(instance)
                else:  # add or update use add
                    session.add(instance)
                await session.commit()
                await session.refresh(instance)
                code = 1
        except Exception as e:
            error = e

        finally:
            return await endpoint_output(instance, code, error)


# @cache(expire=ONE_DAY_SEC, namespace='sms_gets')  # Cache for 1 day
async def sms_gets(sms_class: Type[Result], action: str = "first", idx: str = None, stmt: SelectOfScalar[Type[Result]] = None) -> Union[ErrorResponse, EndpointResponse]:
    async with AsyncSession(sms_resource["engine"]) as session:
        result = None
        error = None
        code = 1
        try:
            if action == "all":
                statement = select(sms_class) if stmt is None else stmt
                instance_list = (await session.exec(statement)).all()
                if instance_list:
                    result = {
                        str(instance.id): instance for instance in instance_list}
            elif action == "first":
                statement = select(sms_class).where(
                    sms_class.id == idx) if stmt is None else stmt
                result = (await session.exec(statement)).first()

        except Exception as e:
            code = 0
            error = e
        finally:
            return await endpoint_output(result, code, error)


# Student Routes

@app.post('/api/v1/sms/add_student', tags=['Student'])
async def add_student(student: Student) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(student, student.id, action="add")


@app.put('/api/v1/sms/update_student', tags=['Student'])
async def update_student(student: Student) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(student, student.id, action="update")


@app.delete('/api/v1/sms/delete_student', tags=['Student'])
async def delete_student(student: Student) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(student, student.id, action="delete")


@app.get("/api/v1/sms/students/{id}", tags=['Student'])
async def find_student(id: str) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Student, "first", id)


@app.get("/api/v1/sms/students", tags=['Student'])
async def all_students() -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Student, "all")


# Instructor Routes

@app.post('/api/v1/sms/add_instructor', tags=['Instructor'])
async def add_instructor(instructor: Instructor) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(instructor, instructor.id, action="add")


@app.put('/api/v1/sms/update_instructor', tags=['Instructor'])
async def update_instructor(instructor: Instructor) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(instructor, instructor.id, action="update")


@app.delete('/api/v1/sms/delete_instructor', tags=['Instructor'])
async def delete_student(instructor: Instructor) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(instructor, instructor.id, action="delete")


@app.get("/api/v1/sms/instructors/{id}", tags=['Instructor'])
async def find_instructor(id: str) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Instructor, "first", id)


@app.get("/api/v1/sms/instructors", tags=['Instructor'])
async def all_instructors() -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Instructor, "all")


# Course Routes

@app.post('/api/v1/sms/add_course', tags=['Course'])
async def add_course(course: Course) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(course, course.id, action="add")


@app.put('/api/v1/sms/update_course', tags=['Course'])
async def update_course(course: Course) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(course, course.id, action="update")


@app.delete('/api/v1/sms/delete_course', tags=['Course'])
async def delete_student(course: Course) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(course, course.id, action="delete")


@app.get("/api/v1/sms/courses/{id}", tags=['Course'])
async def find_course(id: str) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Course, "first", id)


@app.get("/api/v1/sms/courses", tags=['Course'])
async def all_courses() -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Course, "all")


# Enroll Routes

@app.post('/api/v1/sms/enroll_student', tags=['Enroll'])
async def enroll_student(enrollment: Enrollment) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(enrollment, enrollment.id, action="add")


@app.put('/api/v1/sms/update_enrolled_student', tags=['Enroll'])
async def update_enrolled_student(enrollment: Enrollment) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(enrollment, enrollment.id, action="update")


@app.delete('/api/v1/sms/delete_enrolled_student', tags=['Enroll'])
async def delete_enrolled_student(enrollment: Enrollment) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(enrollment, enrollment.id, action="delete")


@app.get('/api/v1/sms/enrollments/{id}', tags=['Enroll'])
async def find_enrollment_by_id(id: str) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Enrollment, "first", id)


@app.get('/api/v1/sms/enrollments/{student_id}', tags=['Enroll'])
async def find_enrollment_by_student_id(student_id: str) -> Union[ErrorResponse, EndpointResponse]:
    stmt = select(Enrollment).where(Enrollment.student_id == student_id)
    return await sms_gets(Enrollment, action="all", stmt=stmt)


@app.get('/api/v1/sms/enrollments', tags=['Enroll'])
async def all_enrolled_students() -> Union[ErrorResponse, EndpointResponse]:
    return await sms_gets(Enrollment, "all")


@app.put('/api/v1/sms/grade_student', tags=['Grade'])
async def assign_grade(enrollment: Enrollment) -> Union[ErrorResponse, EndpointResponse]:
    return await sms_posts(enrollment, enrollment.id, action="update")
