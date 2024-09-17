import requests
import json
import argparse
import os
import shutil
import subprocess
import re
import sys
# NO SSH
# BUT we ask AI to check carefully about each step it has done

error_limit = 5
pyfile_limit = 12

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "*****"  # Replace 'your-api-key' with your API key
}

def get_file_names():
    files_and_dirs = os.listdir('.')
    files = [f for f in files_and_dirs if os.path.isfile(f)]
    files_str = ' '.join(files)
    return files_str

def prompt_extract(str1):
    # Match code block that starts with ```python and ends with ```, ignoring case
    match = re.search(r'<<<prompt(.*?)>>>', str1, re.DOTALL | re.IGNORECASE)
    if match:
        substr = match.group(1)  # Extracted content
    else:
        substr = "No prompt found."
    return substr

def subtask_extract(str1):
    # Match code block that starts with ```python and ends with ```, ignoring case
    match = re.search(r'<<<subtask(.*?)>>>', str1, re.DOTALL | re.IGNORECASE)
    if match:
        substr = match.group(1)  # Extracted content
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
    with open("py"+str(N_py)+".py", "w", encoding='UTF-8') as f:
        f.write(pystr)

    # Execute py1.py script in the background, capturing output and errors
    process = subprocess.Popen(["python", "py"+str(N_py)+".py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()

    return output, error

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
##### main ai
mainai_header =  "You are the main AI, tasked with generating prompts for subtasks based on the provided overall mission description. These prompts will be executed by several subordinate AIs. Instructions:(1) Begin your response by declaring, ‘I am the main AI.’(2) Outline 2-3 subtasks derived from the overall mission.(3) Craft the prompt for the first subtask, commencing with '<<<prompt' and concluding with 'end>>>', requiring the subordinate AI to provide a complete and executable Python program to accomplish this subtask. [General mission Description:]"
CONTENT = mainai_header + code_str
CONTENT = CONTENT
data = {
    "model": "gpt-4-turbo",
    "messages": [{"role": "user", "content": CONTENT}]
}
response = requests.post(url, headers=headers, data=json.dumps(data))
str1 = response.json()['choices'][0]['message']['content'].strip()
print('##### main ai answer:\n',str1)
conversation_main = []
conversation_main.append({"role": "user", "content": CONTENT})
conversation_main.append({"role": "assistant", "content": str1})
str_prompt = prompt_extract(str1)

##### sub ai
subai_header = "You are a sub-AI tasked with executing a sub-task within a larger task. Requirements are as follows: (1) Begin your response by stating, 'I am a sub-AI.' (2) This sub-task necessitates that you write a complete, executable Python program. (3) Include print statements to display crucial outputs for subsequent sub-tasks (this is essential). (4) Commence your Python code with '```python\n' and end with '```'. [Sub-task Description:]"
CONTENT = subai_header + str_prompt
CONTENT = CONTENT
data = {
    "model": "gpt-4-turbo",
    "messages": [{"role": "user", "content": CONTENT}]
}
response = requests.post(url, headers=headers, data=json.dumps(data))
str1 = response.json()['choices'][0]['message']['content'].strip()
print('##### sub ai answer:\n',str1)
conversation = []
conversation.append({"role": "user", "content": CONTENT})
conversation.append({"role": "assistant", "content": str1})
# conversation_main.append({"role": "user", "content": CONTENT})
# conversation_main.append({"role": "assistant", "content": str1})
str_py1 = pystr_extract(str1)
str_prompt = prompt_extract(str1)
# examination
CONTENT = "Examine the given Python code to verify its flawless execution of the assigned subtask outlined in the provided subtask description. Respond accordingly: (1) If the code is perfect, reply only with 'YES' (in uppercase). (2) Otherwise, improve the code and submit the fully updated version. [Python Code]:"+str_py1+" [subtask description]:"+str_prompt
conversation.append({"role": "user", "content": CONTENT})
data = {
    "model": "gpt-4-turbo",
    "messages": conversation
}
response = requests.post(url, headers=headers, data=json.dumps(data))
str1 = response.json()['choices'][0]['message']['content'].strip()
print('###### examination:\n',str1)
conversation.append({"role": "assistant", "content": str1})
# conversation_main.append({"role": "assistant", "content": str1})
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
    Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements.[sub task]:" + str_prompt
    CONTENT = Str_header

    conversation.append({"role": "user", "content": CONTENT})
    # conversation_main.append({"role": "user", "content": CONTENT})
    data = {
        "model": "gpt-4-turbo",
        "messages": conversation
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str1 = response.json()['choices'][0]['message']['content']
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
    conversation_main.append({"role": "assistant", "content": 'sub ai :'+str1+'\npython output:'+str(output)})
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
    ##### main ai
    mainai_header =  "You are the main AI. Provide the next sub-task for the sub-AI to execute, or proceed only once all subtasks have been completed. Instructions:(1) Begin your response by declaring, ‘I am the main AI.’(2) Craft the prompt for the next subtask, commencing with '<<<prompt' and concluding with 'end>>>', requiring the subordinate AI to provide a complete and executable Python program to accomplish this subtask. [Previous Step Output]"
    CONTENT = mainai_header + output + ".[Current directory file names]:" + files_str + ". [general mission Description]:" + code_str
    CONTENT = CONTENT
    conversation_main.append({"role": "user", "content": CONTENT})
    data = {
        "model": "gpt-4-turbo",
        "messages": conversation_main
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str1 = response.json()['choices'][0]['message']['content']
    print('##### answer:\n',str1)
    conversation_main.append({"role": "assistant", "content":str1})
    str_prompt = prompt_extract(str1)

    ##### sub ai
    subai_header = "You are a sub-AI tasked with executing a sub-task within a larger task. Requirements are as follows: (1) Begin your response by stating, 'I am a sub-AI.' (2) This sub-task necessitates that you write a complete, executable Python program. (3) Take note to examine the files already present in the folder, which may be outputs from the previous sub-task and could be beneficial in accomplishing the current one. (4) Include print statements to display crucial outputs for subsequent sub-tasks (this is essential). (5) Commence your Python code with '```python\n' and end with '```'. [Sub-task Description:]"
    CONTENT = subai_header + str_prompt
    CONTENT = CONTENT
    data = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": CONTENT}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str1 = response.json()['choices'][0]['message']['content'].strip()
    print('##### sub ai answer:\n', str1)
    conversation = []
    conversation.append({"role": "user", "content": CONTENT})
    conversation.append({"role": "assistant", "content": str1})
    # conversation_main.append({"role": "user", "content": CONTENT})
    # conversation_main.append({"role": "assistant", "content": str1})
    str_py1 = pystr_extract(str1)
    str_prompt = prompt_extract(str1)
    # examination
    CONTENT = "Examine the given Python code to verify its flawless execution of the assigned subtask outlined in the provided subtask description. Respond accordingly: (1) If the code is perfect, reply only with 'YES' (in uppercase). (2) Otherwise, improve the code and submit the fully updated version. (3) If asked to write in a Word doc, ensure completeness (each section must contain the required word count). [Python Code]:" + str_py1 + " [subtask description]:" + str_prompt
    conversation.append({"role": "user", "content": CONTENT})
    data = {
        "model": "gpt-4-turbo",
        "messages": conversation
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    str1 = response.json()['choices'][0]['message']['content'].strip()
    print('##### examiniation:\n',str1)
    conversation.append({"role": "assistant", "content": response.json()['choices'][0]['message']['content']})
    if str1=='YES':
        str_py1=str_py1
    else:
        str_py1 = pystr_extract(str1)
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
        Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements.[sub task]:" + str_prompt
        CONTENT = Str_header
        CONTENT = CONTENT
        conversation.append({"role": "user", "content": CONTENT})
        data = {
            "model": "gpt-4-turbo",
            "messages": conversation
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        str1 = response.json()['choices'][0]['message']['content'].strip()
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
        conversation_main.append({"role": "assistant", "content": 'sub ai :' + str1 + '\npython output:' + str(output)})
    if k_error >= error_limit:
        print('Mission failed.')
        sys.exit()
    files_str = get_file_names()
    kk+=1
    print('Step '+ str(kk+1)+' is finished')

print('Mission is completed')
