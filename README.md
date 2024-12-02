# 1. Autonomous simulation agent (ASA)
**ASA** is a general-purpose **end-to-end simulation agent** that can **independently complete simulation-related tasks across different sientific domains**, as long as the user provides a **text-based Research Plan (RP)**.

ASA utilizes an automatic program **AutoProg**, which is based on Python3 to interact with **Large Language Models (LLMs)** (via API) through prompt engineering, following a pre-designed logic. At different stages of the automated process, AutoProg prompts the LLM to respond accordingly. Thus, according to the RP provided by the user, ASA can automatically execute end-to-end simulation research processes that include computer simulations based on Python, data statistics, plotting, and report writing.

# 1.1 Paper Information
In our paper, we designed several RPs to demonstrate the power of ASA, which are related to the following problems:
- **Polymer chain conformation simulation:** RP 1-3 ([SI-data-1](/SI-data-1)), Manager-Executor AI mode and Multitier RP mode ([SI-data-2](/SI-data-2))
- **Gravitational simulation:** RP S1-S2 ([SI-data-3](/SI-data-3))

**Our paper is available on [https://arxiv.org/abs/2408.15512](https://arxiv.org/abs/2408.15512).**

[SI.pdf](SI.pdf) provides 1) RP1-3, 2) partial result figures for gravitational simulation mission, and 3) examples of reports written by ASAs. *Please download the raw file to view SI.pdf.

# 2. Writing the Research Plan
The Research Plan is designed by humans and saved in txt file. Users can modify or replace it according to their own tasks. When modifying or replacing the RP, please note that ASA will execute the process based on the content of the RP. To improve the quality of ASA's task completion, the RP should contain as detailed information as possible, including the simulation methods required for the AI to use in the simulation program, modeling settings, parameter settings, as well as subsequent data processing requirements, plotting, and Word report requirements.

It is important to note that ASA cannot install Python packages locally. Therefore, if packages such as numpy, matplotlib, scipy, and python-docx are needed when ASA executes the tasks described in the RP, users must install them beforehand. (If unsure about what packages to install, one can run ASA once and then install the necessary packages based on the error messages indicating missing packages.)

# 3. LLM API Interface and Account Information
ASA’s AutoProg uses the API interface of LLMs to send prompts and receive responses from the LLMs. In our paper, we have tested the APIs of GPT-4o, GPT-4-Turbo, GPT-3.5-Turbo, SparkDesk-3.5, Llama-3-Sonar, Gemini-1.5-Pro, Claude-3.5, Moonshot, and Qwen2. Users can change the LLM API used in AutoProg according to their preferences. For the specific methods of calling each LLM's API, refer to their official documentation.

Additionally, in the examples provided, we offer AutoProgs configured to use the APIs of GPT-4o, GPT-4-Turbo, and Claude-3.5. However, due to privacy concerns, the API keys used in these examples are masked with '*****'. Before running the examples, users need to apply for API accounts for GPT and Claude from OpenAI and Anthropic respectively, and then replace the API key information to successfully run the examples.

# 4. Running ASA
After confirming that Section 2 and 3 are correctly set up, you can proceed to run ASA.

Place the AutoProg.py and RP.txt files in your working directory, enter the working directory via the terminal, and input the command:

   `python AutoProg.py -s RP.txt > out.txt`
   
ASA will read the contents of the RP and execute the automatic simulation research process according to RP’s requirements. All Python programs written by ASA, along with generated images and Word documents, will be saved in the current working directory. Additionally, ASA will generate an output file to record the conversation history with the LLM and the output and errors of the Python programs it has written.

In this repository we provide partial **AutoProgs and sample result files** for:
- **Sample problem of Random-walk Chain Simulation: RP 1-3** ([SI-data-1](/SI-data-1))
- **Manager-Executor AI mode and Multitier RP mode** ([SI-data-2](/SI-data-2))
- **Challenging problem of Universal Gravitation Simulation: RP S1-S2** ([SI-data-3](/SI-data-3))

***AutoProg Notice:** **API account and server information has been obscured in the AutoProg.py**; you can replace it with your own information and follow the instructions to run the AutoProgs.

## 4.1 SI-data-1: AutoProgs for Sample problem of Random-walk Chain Simulation
[SI-data-1](/SI-data-1) includes partial AutoProgs and experimental result files for **RP 1-3**.
- **RP 1** requires generating a Python program to simulate a random walk, sampling different numbers of chain segments *N*, deriving the scaling relation $\left \langle R^2 \right \rangle \propto N^v$, saving chain conformation graphs and scaling relation fit plots, and writing a research report.
- **RP 2** directly provides a random walk simulation program, asking the ASA to modify it, run simulations in a designated folder on a remote server, download the experimental data, and generate graphs and plots and a research report.
- **RP 3** is similar to RP 1 but includes both random walk and self-avoiding walk simulations.

## 4.2 SI-data-2: AutoProgs for Manager-Executor AI mode and Multitier RP mode
[SI-data-2](/SI-data-2) includes partial AutoProgs and experimental result files for **Manager-Executor AI mode and Multitier RP mode**.
- **Manager-Executor AI mode:** In the preceding section, the ASA used a single AI to execute all the content provided in the RP given by human. In this section, we adjusted the logic for storing and managing dialogue history with the LLM within the ASA. We introduced a Manager AI that automatically breaks down a human-provided RP into sub-tasks and distributes them as sub-RPs to multiple Executor AIs. Each Executor AI is unaware of the dialogue history of the Manager AI and other Executor AIs, focusing solely on executing the assigned sub-RP. In contrast, the Manager AI solely presents the sub-RPs and receives reports upon task completion.
- **Multitier RP mode:** In this section, we automate multiple rounds of RP 1 execution. We designed **RP4**, which is nested within RP 1, instructing a Primary AI to execute the command “python AutoProg.py -s p1.txt -n i” 20 times. Each execution generates an
Agent AI to fulfill RP 1 contained in p1.txt, while the Primary AI collects all generated files and conducts result analysis.

## 4.3 SI-data-3: AutoProgs for Challenging problem of Universal Gravitation Simulation
[SI-data-3](/SI-data-3) includes partial AutoProgs and experimental result files for **RP S1-S2**.
- **RP S1** requires using the Skyfield Python library (which needs to be pre-installed via pip) to obtain information on the position, velocity, and mass of certain celestial bodies in the Solar System on January 1, 2024. Using the gravitational formula $U=-\frac{G\cdot m_{1}\cdot m_{2}}{r^{\beta}}$, it requires simulating the motion of these bodies over the next year, with $\beta$ set to 1 and 1.001 respectively, plotting the trajectories of the celestial bodies and writing a report on the findings.
- **RP S2** requires finding a Python library to obtain information of more celestial bodies in the Solar System. Additionally, assuming an asteroid is moving towards Earth from a certain location, it requires simulating the motion of these bodies, including the asteroid, over the next year, plotting the trajectories of them and creating a distance curve between the Earth and the asteroid, and finally writing a report.

# 5. Demo video
Additionally, we have created a **demo video** ([SI-video.mp4](SI-video.mp4)) demonstrating the operation process of the automatic research system.
*Please download the raw file to watch the demo video.
