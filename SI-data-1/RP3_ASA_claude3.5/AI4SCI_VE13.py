import requests
import json
import argparse
import os
import shutil
import subprocess
import re
import time
import sys
import anthropic
# NO SSH
# BUT we ask AI to check carefully about each step he has done

error_limit = 5
pyfile_limit = 12

MODEL = "claude-3-5-sonnet-20240620"
MAX_TOKENS = 4096
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="*****",
)

def get_file_names():
    files_and_dirs = os.listdir('.')
    files = [f for f in files_and_dirs if os.path.isfile(f)]
    files_str = ' '.join(files)
    return files_str

def subtask_extract(str1):
    # Match code block that starts with ```python and ends with ```, ignoring case
    match = re.search(r'<<<subtask(.*?)>>>', str1, re.DOTALL | re.IGNORECASE)
    if match:
        substr = match.group(1)  # Extracted Python code
    else:
        substr = "No Sub Task found."
    return substr

def pystr_extract(str1):
    # Match code block that starts with ```python and ends with ```, ignoring case
    match = re.search(r'```python\n(.*?)```', str1, re.DOTALL | re.IGNORECASE)
    if match:
        pystr = match.group(1)  # Extracted Python code
    else:
        pystr = "No Python code found."
    return pystr

def execute_script(pystr,N_py, timeout=30*60):
    # Save the code to py1.py
    with open("py"+str(N_py)+".py", "w", encoding='UTF-8') as f:
        f.write(pystr)
    output = None
    error = None
    try:
        # Execute py1.py script in the background, capturing output and errors
        process = subprocess.Popen(["python", "py"+str(N_py)+".py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Monitor the process for timeout
        start_time = time.time()
        while True:
            if process.poll() is not None:  # Check if the process has finished
                break
            if time.time() - start_time > timeout:
                print("Timeout reached, terminating the subprocess.")
                process.terminate()
                process.wait(timeout=5)  # Wait for the process to terminate, give it 5 seconds grace period
                output = "TimeoutError: The subprocess took too long to execute."
                error = "TimeoutError: The subprocess took too long to execute."
                break
            time.sleep(10)  # Sleep for a short interval before checking again

        # If we didn't time out, collect the output and errors
        if output is None and error is None:
            output, error = process.communicate()

    except Exception as e:
        output = str(e)
        error = str(e)

    finally:
        return output, error
        pass

# Create a parser
parser = argparse.ArgumentParser(description='Process some file.')
parser.add_argument('-s', metavar='filename', type=str, help='the name of the file or string to process')
args = parser.parse_args()
filename = args.s
if filename.endswith(".txt") and ' ' not in filename:
    with open(filename, 'r') as file:
        code_str = file.read()
else:
    code_str = filename

N_py=1


"""
Modal I: Task split
"""
Str_header = "Carefully review the task description below, as you'll create multiple Python programs. Ensuring: (1) Provide a complete, executable program tailored exactly to the task, not a sample. (2) Include print statements to show key outputs for later tasks (essential). (3) Begin your Python code with '```python\n' and end with '```'. (4) Extract all subtask details for the first program using '<<<subtask' and '>>>'. [Task Description:]"
CONTENT = Str_header + code_str
CONTENT = CONTENT
messages = [{"role": "user", "content": CONTENT}]
response = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    messages=messages
)
str1 = response.content[0].text
print('##### answer:\n',str1)
conversation = []
conversation.append({"role": "user", "content": CONTENT})
conversation.append({"role": "assistant", "content": str1})
str_py1 = pystr_extract(str1)
str_sub = subtask_extract(str1)
CONTENT = "Examine the given Python code to verify its flawless execution of the assigned subtask outlined in the provided subtask description. Respond accordingly: (1) If the code is perfect, reply only with 'YES' (in uppercase). (2) Otherwise, improve the code and submit the fully updated version. [Python Code]:"+str_py1+" [subtask description]:"+str_sub
conversation.append({"role": "user", "content": CONTENT})
response = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    messages=conversation
)
str1 = response.content[0].text
print('###### examination:\n',str1)
conversation.append({"role": "assistant", "content": str1})
if str1=='YES':
    str_py1=str_py1
else:
    str_py1 = pystr_extract(str1)

print('Begin to execute Python')
output, error = execute_script(str_py1,N_py)
N_py+=1
if N_py > pyfile_limit:
    print('Mission failed.')
    sys.exit()
k_error = 0
while error:
    print(f"Error: {error}")
    Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements.[sub task]:" + str_sub
    CONTENT = Str_header

    conversation.append({"role": "user", "content": CONTENT})
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=conversation
    )
    str1 = response.content[0].text
    print('##### correction:\n',str1)
    conversation.append({"role": "assistant", "content": str1})

    str_py1 =  pystr_extract(str1)
    print('Begin to execute Python ' + str(k_error))
    output, error = execute_script(str_py1,N_py)
    N_py+=1
    if N_py > pyfile_limit:
        print('Mission failed.')
        sys.exit()
    k_error += 1
    if k_error > error_limit: break
if k_error < error_limit:
    print(f"Output: {output}")
if k_error >= error_limit:
    print('Mission failed.')
    sys.exit()

# Obtain the file names
files_str = get_file_names()

"""
Section II: Number of programs
"""
kk=0
print('Step '+ str(kk+1)+' is finished')
while str_py1 != "No Python code found.":
    Str_header = "Begin writing either the second or third program, or proceed only after completing all tasks. Ensuring: (1) Provide a complete, executable program tailored exactly to the task, not a sample. (2) Consider the output from the prior step and filenames in the current directory, as they might be results from the previous program and potentially useful in the current one. (3) Extract all subtask details for the current program using '<<<subtask' and '>>>'. [Previous Step Output]:"

    CONTENT = Str_header + output + ".[Current directory file names]:" + files_str  + ". [previous Task Description]:" + code_str
    CONTENT = CONTENT
    conversation.append({"role": "user", "content": CONTENT})

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=conversation
    )
    str2 = response.content[0].text
    print('##### answer:\n',str2)
    conversation.append({"role": "assistant", "content":str2})
    str_py2 = pystr_extract(str2)
    str_sub = subtask_extract(str2)
    CONTENT = "Examine the given Python code to verify its flawless execution of the assigned subtask outlined in the provided subtask description. Respond accordingly: (1) If the code is perfect, reply only with 'YES' (in uppercase). (2) Otherwise, improve the code and submit the fully updated version. (3) If asked to write in a Word doc, ensure completeness (each section must contain the required word count). [Python Code]:" + str_py2 + " [subtask description]:" + str_sub
    conversation.append({"role": "user", "content": CONTENT})
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=conversation
    )
    str2 = response.content[0].text
    print('##### examiniation:\n',str2)
    conversation.append({"role": "assistant", "content": str2})
    if str2=='YES':
        str_py1=str_py2
    else:
        str_py1 = pystr_extract(str2)
    if str_py1 == "No Python code found.":
        print('Mission complete.')
        sys.exit()
    print('Begin to execute Python')
    output, error = execute_script(str_py1,N_py)
    N_py+=1
    if N_py > pyfile_limit:
        print('Mission failed.')
        sys.exit()
    k_error = 0
    while error:
        print(f"Error: {error}")
        Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements.[sub task]:" + str_sub
        CONTENT = Str_header
        CONTENT = CONTENT
        conversation.append({"role": "user", "content": CONTENT})
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=conversation
        )
        str1 = response.content[0].text
        print('##### correction:\n',str1)
        conversation.append({"role": "assistant", "content": str1})
        str_py1 =  pystr_extract(str1)
        print('Begin to execute Python ' + str(k_error))
        output, error = execute_script(str_py1,N_py)
        N_py+=1
        if N_py > pyfile_limit:
            print('Mission failed.')
            sys.exit()
        k_error += 1
        if k_error > error_limit: break
    if k_error < error_limit:
        print(f"Output: {output}")
    if k_error >= error_limit:
        print('Mission failed.')
        sys.exit()
    files_str = get_file_names()
    kk+=1
    print('Step '+ str(kk+1)+' is finished')

print('Mission is completed')
