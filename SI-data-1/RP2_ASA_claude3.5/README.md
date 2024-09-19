# Before running ASA
- Please obtain the Python SDK from the official Claude documentation.
- Download the following Python packages: numpy, matplotlib, scipy, python-docx, paramiko.
- Replace the API key in AI4SCI_V22.py and remote node information in p2.txt with yours.

# Windows CMD command to run ASA
```python AI4SCI_V22.py -s p2.txt > out.txt```

AutoProg AI4SCI_V22.py will read the RP in p2.txt and autonomously run the simulation research process. The LLM conversation history is stored in out.txt. 

**You can replace the content of p2.txt with your own RP to initiate your research process.**
