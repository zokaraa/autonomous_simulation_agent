import requests
import json
import argparse
import os
import shutil
import subprocess
import re
import sys
# NO SSH
# BUT we ask AI to check carefully about each step he has done


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

def execute_script(pystr,N_py):
    # Save the code to py1.py
    with open("./try"+str(trynumber)+"/py"+str(N_py)+".py", "w", encoding='UTF-8') as f:
        f.write(pystr)

    # Execute py1.py script in the background, capturing output and errors
    print(f'execute py{str(N_py)}.py')
    process = subprocess.Popen(["python", "./try"+str(trynumber)+"/py"+str(N_py)+".py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print('output:')
    print(output)
    print('error:')
    print(error)
    return output, error

# Create a parser
parser = argparse.ArgumentParser(description='Process some file.')
parser.add_argument('-s', metavar='filename', type=str, help='the name of the file or string to process')
parser.add_argument('-n', metavar='trynumber', type=str, help='the trail number of the experiment')
args = parser.parse_args()
filename = args.s
trynumber = args.n
if filename.endswith(".txt") and ' ' not in filename:
    with open(filename, 'r') as file:
        code_str = file.read()
else:
    code_str = filename

url = "https://api.openai.com/v1/chat/completions"
N_py=1
headers = {
    "Content-Type": "application/json",
    "Authorization": "*****"  # Replace 'your-api-key' with your API key
}
error_limit = 5

"""
Modal I: Task split
"""
Str_header = "Please read the following task description carefully; you may need to write several Python programs. Start with the first Python program, with the requirements: (1) provide a complete and executable program, not just a sample, but an accurate program tailored for the task, and (2) ensure to include print statements for some output results to facilitate later tasks. Please remember this point. (3) This point is also important, extract all the sub task details related with the first program from the task description in your response starting with '<<<subtask' and ending with '>>>'. [Task Description]:"
CONTENT = Str_header + code_str
CONTENT = CONTENT
data = {
    "model": "gpt-4-turbo",
    "messages": [{"role": "user", "content": CONTENT}]
}
response = requests.post(url, headers=headers, data=json.dumps(data))
str1 = response.json()['choices'][0]['message']['content'].strip()

conversation = []
conversation.append({"role": "user", "content": CONTENT})
conversation.append({"role": "assistant", "content": response.json()['choices'][0]['message']['content']})
str_py1 = pystr_extract(str1)
str_sub = subtask_extract(str1)
CONTENT = "Please carefully examine the following python code to check if it has perfectly finish the subtask as described in the subtask description with the requirements: (1) If the python code is already perfect, please just response three captital letters 'YES' and NOTHING else. (2) If not please make it more perfect and output the complete updated python code. [Python Code]:"+str_py1+" [subtask description]:"+str_sub
conversation.append({"role": "user", "content": CONTENT})
data = {
    "model": "gpt-4-turbo",
    "messages": conversation
}
response = requests.post(url, headers=headers, data=json.dumps(data))
str1 = response.json()['choices'][0]['message']['content'].strip()
conversation.append({"role": "assistant", "content": response.json()['choices'][0]['message']['content']})
if str1=='YES':
    str_py1 = str_py1
else:
    str_py1 = pystr_extract(str1)

print('Begin to execute Python')
output, error = execute_script(str_py1,N_py)
N_py+=1
k_error = 0
while error:
    print(f"Error: {error}")
    Str_header = f"The previous program had errors, , [Error]: {error}. Please correct them. Requirements: provide a corrected, complete, and executable program, accurately tailored for the sub task.[sub task]:"+str_sub
    CONTENT = Str_header

    conversation.append({"role": "user", "content": CONTENT})
    data = {
        "model": "gpt-4-turbo",
        "messages": conversation
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str1 = response.json()['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": str1})

    str_py1 =  pystr_extract(str1)
    print('Begin to execute Python ' + str(k_error))
    output, error = execute_script(str_py1,N_py)
    print(output, error)
    N_py+=1
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
    Str_header = "Start writing the second or third program, or skip only when all tasks has been done. Requirements: (1) Output a complete and executable program, not a sample, but an accurate program STRICTLY following the instructions of the task (2) Please consider the output of the previous step and the file names in the current directory, as they may be the results from the previous program and could be used in writing the current program. (3) This point is also important, extract all the sub task details related with the current program from the task description in your response starting with '<<<subtask' and ending with '>>>'. [Previous Step Output]:"

    CONTENT = Str_header + output + ".[Current directory file names]:" + files_str  + ". [previous Task Description]:" + code_str
    CONTENT = CONTENT
    conversation.append({"role": "user", "content": CONTENT})

    data = {
        "model": "gpt-4-turbo",
        "messages": conversation
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str2 = response.json()['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content":str2})
    str_py2 = pystr_extract(str2)
    str_sub = subtask_extract(str2)
    CONTENT = "Please carefully examine the following python code to check if it has perfectly finish the subtask as described in the subtask description with the requirements: (1) If the python code is already perfect, please just response three captital letters 'YES' and NOTHING else. (2) If not please make it more perfect and output the complete updated python code. (3) If you are ask to write something in word doc, please check if the writing is complete (BE SURE that each section contains sufficient words as required). [Python Code]:"+str_py2+" [subtask description]:"+str_sub
    conversation.append({"role": "user", "content": CONTENT})
    data = {
        "model": "gpt-4-turbo",
        "messages": conversation
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str2 = response.json()['choices'][0]['message']['content'].strip()
    conversation.append({"role": "assistant", "content": response.json()['choices'][0]['message']['content']})
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
    k_error = 0
    while error:
        print(f"Error: {error}")
        Str_header = f"The previous program had errors, [Error]: {error}. Please correct them. Requirements: provide a corrected, complete, and executable program, accurately tailored for the sub task. [sub task]:"+str_sub
        CONTENT = Str_header
        CONTENT = CONTENT
        conversation.append({"role": "user", "content": CONTENT})
        data = {
            "model": "gpt-4-turbo",
            "messages": conversation
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        str1 = response.json()['choices'][0]['message']['content'].strip()
        conversation.append({"role": "assistant", "content": str1})
        str_py1 =  pystr_extract(str1)
        print('Begin to execute Python ' + str(k_error))
        output, error = execute_script(str_py1,N_py)
        N_py+=1
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
