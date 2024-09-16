import requests
import json
import argparse
import os
import shutil
import subprocess
import re
import sys
import anthropic

error_limit = 5
pyfile_limit = 12
MODEL = 'claude-3-5-sonnet-20240620'
MAX_TOKENS = 4096

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key='*****',
)

def get_file_names():
    files_and_dirs = os.listdir('.')
    files = [f for f in files_and_dirs if os.path.isfile(f)]
    files_str = ' '.join(files)
    return files_str

def pystr_extract(str1):
    # Match code block that starts with ```python and ends with ```, ignoring case
    match = re.search(r'```python\n(.*?)```', str1, re.DOTALL | re.IGNORECASE)
    if match:
        pystr = match.group(1)  # Extracted Python code
    else:
        pystr = "No Python code found."
    return pystr

def pynotrun_check(str1):
    return re.search(r'NO-RUN-PY', str1, re.DOTALL | re.IGNORECASE)


def execute_script(pystr,N_py):
    # Save the code to py1.py
    with open("py"+str(N_py)+".py", "w", encoding='UTF-8') as f:
        f.write(pystr)

    # Execute py1.py script in the background, capturing output and errors
    process = subprocess.Popen(["python", "py"+str(N_py)+".py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()

    return output, error

def error_check(conversation,error,N_py):
    k_error = 0
    while error:
        print(f"Error: {error}")
        Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements."
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
        if str_py1 == "No Python code found.":
            print('Mission complete.')
            sys.exit()
        print('Begin to execute Python ' + str(k_error))
        output, error = execute_script(str_py1,N_py)
        print(error,k_error,N_py)
        N_py+=1
        if N_py > pyfile_limit:
            print('Mission failed.')
            sys.exit()
        k_error += 1
        if k_error > error_limit:
            print('Mission failed.')
            sys.exit()
        files_str = get_file_names()
    return conversation,error,N_py


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
Section II: Number of programs
"""
kk=0
str_py1="  "
conversation = []
while str_py1 != "No Python code found.":
    if kk>0:
        Str_header = "Start writing the second or third program, or skip if all tasks have been completed. Follow these requirements: (1) Output a complete and executable program strictly adhering to the task instructions, avoiding sample programs. (2) Consider the output of the previous step and the file names in the current directory, as they may result from the previous program and could be utilized in writing the current program. [Previous Step Output]:"
        CONTENT = Str_header + output + ".[Current directory file names]:" + files_str  + ". [previous Task Description]:" + code_str
        CONTENT = CONTENT
        conversation.append({"role": "user", "content": CONTENT})

    if kk==0:
        Str_header = "Please carefully review the task description below. You will need to create two to three Python programs. Start by crafting the first Python program to meet the following criteria: (1) Ensure the program is complete and executable, tailored precisely to the task's requirements. (2) Include print statements to display output results, aiding in subsequent tasks. Keep this in mind. (3) Begin your Python code with '```python\n' and end with '```'. (4) Check whether the program requires execution. If not, include the statement 'NO-RUN-PY' in your response.[Task Description]:"
        CONTENT = Str_header + code_str
        CONTENT = CONTENT
        conversation.append({"role": "user", "content": CONTENT})

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=conversation
    )
    str1 = response.content[0].text
    print('##### answer:\n',str1)
    conversation.append({"role": "assistant", "content":str1})

    str_py1 = pystr_extract(str1)
    if str_py1 == "No Python code found.":
        print('Mission complete.')
        sys.exit()
    if pynotrun_check(str1):
        with open("py"+str(N_py)+".py", "w", encoding='UTF-8') as f:
            f.write(str_py1)
            output=" ";files_str=" "
        N_py+=1
        if N_py > pyfile_limit:
            print('Mission failed.')
            sys.exit()
        files_str = get_file_names()
    else:
        print('Begin to execute Python')
        output, error = execute_script(str_py1,N_py)
        N_py+=1
        if N_py > pyfile_limit:
            print('Mission failed.')
            sys.exit()
        files_str = get_file_names()
        conversation,error,N_py = error_check(conversation,error,N_py)
    print('Step '+ str(kk+1)+' is finished')
    kk+=1

print('Mission Complete')
