# 1. Autonomous simulation agent (ASA)
This study explores the feasibility of constructing an **autonomous simulation agent (ASA)** powered by LLM to automate an entire simulation research process, from experimental design, remote upload and simulation execution, data analysis, to report compilation, after a **research plan (RP)** is provided to the ASA by human researchers. 

*Notice: ASA is a general-purpose fully autonomous simulation agent that **can independently complete any simulation-related task**, as long as the user provides a detailed RP.

The ASA leverages an **API automation program (AutoProg)** to enable multi-round text interactions with LLMs via API, thus achieving full automation of the research process. ASA can solve problems across different scientific domains. 

In our paper, we designed several RPs to demonstrate the power of ASA, which are related to the following problems:
- **Polymer chain conformation simulation: RP 1-3 ([SI-data-1](/SI-data-1)), Main AI generating RP and Multitier human RP ([SI-data-2](/SI-data-2))**
- **Gravitational simulation: RP S1-S2 ([SI-data-3](/SI-data-3))**

Our paper is available on [https://arxiv.org/abs/2408.15512](https://arxiv.org/abs/2408.15512).

# 2. SI information
[SI.pdf](SI.pdf) provides 1) RP1-3, 2) partial result figures for gravitational simulation mission, and 3) examples of reports written by ASAs.

*Please download the raw file.

# 3. AutoProgs and experimental result files
We provide partial **AutoProgs and experimental result files** for:
- **RP 1-3** ([SI-data-1](/SI-data-1))
- **Main AI generating RP and Multitier human RP** ([SI-data-2](/SI-data-2))
- **RP S1-S2** ([SI-data-3](/SI-data-3)).

AutoProg Notice: API account and server information has been obscured in the AutoProg.py; you can replace it with your own information and follow the instructions to run the AutoProgs.

## 3.1 SI-data-1: AutoProgs for RP 1-3
[SI-data-1](/SI-data-1) includes partial AutoProgs and experimental result files for **RP 1-3**
- **RP 1** requires generating a Python program to simulate a random walk, sampling different numbers of chain segments *N*, deriving the scaling relation $\left \langle R^2 \right \rangle \propto N^v$, saving chain conformation graphs and scaling relation fit plots, and writing a research report.
- **RP 2** directly provides a random walk simulation program, asking the ASA to modify it, run simulations in a designated folder on a remote server, download the experimental data, and generate graphs and plots and a research report.
- **RP 3** is similar to RP 1 but includes both random walk and self-avoiding walk simulations.

## 3.2 SI-data-2: AutoProgs for Main AI generating RP and Multitier human RP
[SI-data-2](/SI-data-2) includes partial AutoProgs and experimental result files for **Main AI generating RP and Multitier human RP**
- **Main AI generating RP:** In the preceding section, RPs were provided by humans. In this section, we task a Main AI with automatically breaking down a human-provided RP into sub-tasks and distributing them as AI RPs to several Subordinate AIs. We provided RP 1 directly to the Master AI, adjusting the ASA to ensure each sub-task was handled by a distinct Subordinate AI without access to the Main AI’s or other Subordinate AIs’ conversation histories. The Main AI solely presents the AI RPs (Figure S1A) and received reports upon task completion.
- **Multitier human RP:** In this section, we automate multiple rounds of RP 1 execution. We designed **RP4**, which is nested within RP 1, instructing a Primary AI to execute the command “python AutoProg.py -s p1.txt -n i” 20 times. Each execution generates an
Agent AI to fulfill RP 1 contained in p1.txt, while the Primary AI collects all generated files and conducts result analysis.

## 3.3 SI-data-3: AutoProgs for RP S1-S2
[SI-data-3](/SI-data-3) includes partial AutoProgs and experimental result files for **RP S1-S2**
- **RP S1** requires using the Skyfield Python library (which needs to be pre-installed via pip) to obtain information on the position, velocity, and mass of certain celestial bodies in the Solar System on January 1, 2024. Using the gravitational formula $U=-\frac{G\cdot m_{1}\cdot m_{2}}{r^{\beta}}$, it requires simulating the motion of these bodies over the next year, with $\beta$ set to 1 and 1.001 respectively, plotting the trajectories of the celestial bodies and writing a report on the findings.

# 4. Demo video
Additionally, we have created a **demo video** ([SI-video.mp4](SI-video.mp4)) demonstrating the operation process of the automatic research system.
*Please download the raw file.
