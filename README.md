# PyCIM simulator

1. To use the SDK, Python 3.7.7 or above is required, and dependencies should be installed according to the requirements.txt after decompression

2. After decompression, there will be a pucim-simulator folder. Copy the simulator to the root path of the project.

3. Use cases can be found in "display.ipynb".

## Installation

```python
git clone https://github.com/shadowforwind/simulator.git
cd simulator
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

## Reference

Refer to "PyCIM: A Python Framework for the Dynamics of Coherent Ising Machine".

Link to https://link.springer.com/chapter/10.1007/978-981-97-5609-4_15