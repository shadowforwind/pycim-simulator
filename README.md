# PyCIM simulator

PyCIM is the first simulator that can produce the dynamic behavior of CIM. PyCIM effectively capture some characteristic phenomena of DOPO and CIM, including a spontaneous symmetry breaking, threshold behavior, gain saturation, and the process of CIM solvingMAX-CUT problems. Additionally, it is built-in time-varying coupling strengths and pump schedules. Moreover, PyCIM can be used for analyzing the impact of parameters on the performance of CIM, and guiding the design and optimization of actual physical systems.

## Requirements

To use the simulator, Python 3.7.7 or above is required.

The following packages are required by the installation:

` matplotlib==3.5.3
` numpy==1.21.5
` scipy==1.7.3

The first step is cloning the repository:

```python
git clone https://github.com/shadowforwind/simulator.git
cd simulator
```

Then, install the following packages:

```python
pip install -r requirements.txt
```

## Catalog

```
└─simulator
    │  architecture.png
    │  display.ipynb
    │  README.md
    │  requirements.txt
    │
    └─pycim
        │  analyzer.py
        │  competitor.py
        │  sampler.py
        │  __init__.py
        │
        ├─data
        │  │  128.txt
        │  │  20.txt
        │
        ├─simulation
        │  │  device.py
        │  │  setup.py
        │  │  simulate.py
        │  │  solver.py
        │  │  __init__.py
        │  │
        │  ├─model
        │  │  │  c_number.py
        │  │  │  discrete.py
        │  │  │  meanFiled.py
        │  │  │  __init__.py
        │
        ├─utils
        │  │  const.py
        │  │  file_J.py
        │  │  getIsingEnergy.py
        │  │  __init__.py
```

## Getting started with Intel-QS

The simplest way of familiarize with the pycim-simulator is by exploring the demo case provided in the file ''display.ipynb''. The file ''display.ipynb'' provides step-by-step description of the main commands to: initialize input, transform model, single simulation, result measurement, or solving the Max-Cut problem.

## How to contribute or contact us

Thanks for your interest in the project! If you have a question or want to discuss something, feel free to send an email to [Peixiang Li](peixiangli@quanta.org.cn), [Dongyang Wang](dongyangwang@quanta.org.cn), or to [Junjie Wu](junjiewu@nudt.edu.cn).

## How to cite

When using pycim simulator for research projects, please cite:

Li, P., Cheng, H., Liu, Y., Wang, D., Wu, J. (2024). PyCIM: A Python Framework for the Dynamics of Coherent Ising Machine. In: Huang, DS., Zhang, C., Guo, J. (eds) Advanced Intelligent Computing Technology and Applications. ICIC 2024. Lecture Notes in Computer Science, vol 14871. Springer, Singapore. https://doi.org/10.1007/978-981-97-5609-4_15