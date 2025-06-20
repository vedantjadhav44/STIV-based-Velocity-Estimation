# Velocity Estimation

[![PyPI](https://badge.fury.io/py/pyopenrivercam.svg)](https://pypi.org/project/pyopenrivercam)
[![Conda-Forge](https://anaconda.org/conda-forge/pyopenrivercam/badges/version.svg)](https://anaconda.org/conda-forge/pyopenrivercam)
[![codecov](https://codecov.io/gh/localdevices/pyorc/branch/main/graph/badge.svg?token=0740LBNK6J)](https://codecov.io/gh/localdevices/pyorc)
[![docs_latest](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://localdevices.github.io/pyorc/latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/localdevices/pyorc.git/main?labpath=examples)
[![License](https://img.shields.io/github/license/localdevices/pyorc?style=flat)](https://github.com/localdevices/pyorc/blob/main/LICENSE)
[![downloads](https://img.shields.io/pypi/dm/pyopenrivercam)](https://pypi.org/project/pyopenrivercam/)

This work is based on [pyORC](https://github.com/localdevices/pyorc) library for implementation of LSPIV and STIV based flow analysis.

![example_image](https://raw.githubusercontent.com/localdevices/pyorc/main/docs/ngwerere.jpg)
Image: Example of pyorc velocimetry over Ngwerere river at the Zambezi Road crossing - Lusaka, Zambia.

Current capabilities are:
* Reading of frames and reprojection to surface
* Velocimetry estimation at user-defined resolution
* Plotting of velocimetry results  in camera, geographical and orthoprojected perspectives.

We use the well-known **xarray** data models and computation pipelines (with dask) throughout the entire library to
guarantee an easy interoperability with other tools and methods, and allow for lazy computing.

## Installation

Pre-requisites : 
- GCC >=8.4
- Conda (miniforge or miniconda)
- Upgrade PIP and Conda 
- install ipykernal for vscode to run ipynb files. 
- install pylance extension for vscode 

Every command given bellow is to be done on miniforge prompt and not cmd

##### Using PIP
create an environment
```cmd
python -m venv pyorc_env
pyorc_env\Scripts\activate
```

install the required files 
```cmd
pip install pyopenrivercam[extra]
```

update the files if necessary 
```cmd
pip install --upgrade pyopenrivercam[extra]
```

above three steps complete the installation of the libraries
clone the github if you want to test the examples 

For other ways of installation refer to [pyORC GitHub Repository ](https://github.com/localdevices/pyorc)

| Package    | Version | License                            |
|------------|---------|------------------------------------|
| ffpiv      | 0.1.2   | AGPLv3                             |
| numpy      | 1.26.4  | BSD License                        |
| opencv2    | 4.10.0  | MIT License                        |
| openpiv    | 0.25.3  | GPLv3                              |
| matplotlib | 3.9.2   | Python Software Foundation License |
| geopandas  | 1.0.1   | BSD License                        |
| pandas     | 2.2.2   | BSD License                        |
