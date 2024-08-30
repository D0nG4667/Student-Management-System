import io
import sys

# Save the default stdout
default_stdout = sys.stdout

# Set the standard output to UTF-8 encoding, allowing emojie to print to terminal without errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
