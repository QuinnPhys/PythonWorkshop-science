# EQuS Workshop on Python for Quantum Information Science #

*The EQuS Workshop on Python for Quantum Information Science is dedicated to a harassment-free workshop experience for everyone. Our anti-harassment policy can be found
[here](code-of-conduct.md).*

**November 17 & 18, 2016**. Due to space constraints, registration is now closed.

Two-day workshop as an introduction to Python for scientific computing. Please bring your own computer to this event.

## Schedule ##

| | Thursday | | Friday |
|---|---|---|---|
| 9am to 10:30am | Tools for Scientific Computing 0 <br> *Sarah Kaiser* | 9am to 10:30am | Open Systems w/ QuTiP <br> *Chris Granade* |
| 10:30am to 11am | Coffee | 10:30am to 11am | Coffee |
| 11m to 12:30pm | Tools for Scientific Computing 1 <br> *Chris Granade* | 11m to 12:30pm | Data Analysis w/ QInfer <br> *Chris Ferrie* |
| 12:30pm to 1:30pm | Lunch | 12:30pm to 1:30pm | Lunch |
| 1:30pm to 3:00pm | Python for General Use <br> *Sarah Kaiser* | 1:30pm to 3:00pm | Instrument Control <br> *Sarah Kaiser* |
| 3:00pm to 3:30pm | Coffee | 3:00pm to 3:15pm | Coffee |
| 3:30pm to 5:00pm | Python for Scientific Computing <br> *Yuval Sanders* | 3:15pm to 4:00pm | Interoperability <br> *Chris Grande* |
| | | 4:00pm– | Post-workshop social gathering |

## Outline ##

### Thursday ###

- [**Tools for Scientific Computing 0**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-0-scicomp-tools-part0.ipynb)
    - Learn what a **shell** is and how to interact with the **command line**
    - Install and learn about **package managers** 
    - Install and explore two great examples of **modern text editors**
    - Install and set up **Python** for the following lectures

- [**Tools for Scientific Computing 1**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-1-scicomp-tools-part1.ipynb)
    - **Secure shell** (SSH) for remote and HPC computing
    - Version control with **Git**
   
- [**Python for General Use**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-2-python-general.ipynb)
    - Introduction to the **Python** language via an interactive interpreter
    - Learn about **types, indexing, functions, and classes** in Python
    - Python 2 vs. 3
    - **Stylistic guidelines** for keeping collaborators happy (incl. future you)
    - Learn about coding interface called *Jupyter Notebook*

- [**Python for Scientific Computing**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-3-python-scicomp.ipynb)
    - Storing, representing, and manipulating tensors of numeric data with the **NumPy** and **SciPy** packages
    - R-style data analysis with the **Pandas** package
    - publication-quality plotting and with **Matplotlib**, and statistics plotting with **Seaborn**

### Friday ###

- [**Open Quantum Systems Simulation with QuTiP**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-4-qutip.ipynb)
    - Install and configure compilers for use with Python
    - Install **QuTiP** and learn how to represent **quantum states, measurements, unitaries,** and **superoperators**
    - Use QuTiP to examine properties of **norms**
    - See an example of *unit testing* in action

- [**Data Analysis with QInfer**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-5-qinfer.ipynb)
    - Estimate the bias of a classical coin
    - Learn how to use QInfer to perform:
        - **quantum state tomography**
        - **phase estimation**
        - **randomized benchmarking**
    - Specify **custom models** to use with QInfer

- [**Instrument Control with InstrumentKit**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-6-python-instrument-control.ipynb)
    - Learn about **unit support** for calculations in Python via two packages (Quantities and Pint)
    - Go deeper into **classes** in Python and how they can be useful for designing interfaces to communicate to instruments
    - **Design a driver** for a demo instrument 
    
- [**Interoperability with Modern and Legacy Environments**](https://nbviewer.jupyter.org/github/QuinnPhys/PythonWorkshop-science/blob/master/lecture-7-interoperability.ipynb)
    - Connecting Python to **C, MATLAB,** and **Julia**

## Before the Workshop ##

- Please help us save time by downloading the following files, depending on your operating system.
    - Windows 7 or later
        - [Anaconda 4.2.0 for Python 2.7](https://repo.continuum.io/archive/Anaconda2-4.2.0-Windows-x86_64.exe)
        - [Sublime Text 3](https://download.sublimetext.com/Sublime%20Text%20Build%203126%20x64%20Setup.exe)
        - [VS Code 1.7.1](https://go.microsoft.com/fwlink/?LinkID=623230)
    - OS X 10.7 or later
        - [Anaconda 4 for Python 3.5](https://repo.continuum.io/archive/Anaconda3-4.2.0-MacOSX-x86_64.pkg)
        - [Sublime Text 3](https://download.sublimetext.com/Sublime%20Text%20Build%203126.dmg)
        - [VS Code 1.7.1](https://go.microsoft.com/fwlink/?LinkID=760868)
    - Ubuntu 16.04
        - [Anaconda 4 for Python 3.5](https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh)
        - [Sublime Text 3](https://download.sublimetext.com/sublime-text_build-3126_amd64.deb)
        - [VS Code 1.7.1](https://go.microsoft.com/fwlink/?LinkID=620882)

## Additional Resources ##

### Documentation ###

- Style Guides and Best Practices
    - [PEP 8](https://www.python.org/dev/peps/pep-0008/): documents how to
      write clear and legible Python code.
    - [GitHub Flow](https://guides.github.com/introduction/flow/): Suggestions and cultural practices for managing Git branches and merges.
    - [Good Enough Practices in Scientific Computing](https://arxiv.org/abs/1609.00037): Suggestions on how to make the data you want to see in the world.

### Cheatsheets and References ###

- [EPQIS16 Cheatsheet](https://github.com/QuinnPhys/PythonWorkshop-science/raw/master/cheatsheets/python-cheatsheet.pdf): Custom cheatsheet detailing topics covered in this workshop.

### Blog Posts and Lecture Notes ###

Below, we list some blog posts and lecture notes that may be useful as
references, or in digging deeper into the topics presented at the EPQIS
workshop. 

- SSH and Git Configuration
    - [Using SSH Keys in Visual Studio Code on Windows](http://www.cgranade.com/blog/2016/06/06/ssh-keys-in-vscode.html)
    - [Browser-based Git tutorial via GitHub](https://try.github.io/levels/1/challenges/1)
- Python
    - [Learning Python](https://www.codecademy.com/learn/python)
- Text Editors
    - [Simple Visual Enhancements for Better Coding in Sublime Text](https://webdesign.tutsplus.com/articles/simple-visual-enhancements-for-better-coding-in-sublime-text--webdesign-18052)

### Publicity ###

- [Announcement poster](publicity/announcement-poster.pdf)

## Licenses and Attributions ##

The [Git logo by Jason Long](https://git-scm.com/downloads/logos) is used under the Creative Commons BY 3.0 license.
