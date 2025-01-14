# Trading Simulator
[![Python Build](https://github.com/mathieugouin/tradesim/actions/workflows/ci.yml/badge.svg)](https://github.com/mathieugouin/tradesim/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mathieugouin/tradesim/branch/master/graph/badge.svg?token=4ZZ9V7NU91)](https://codecov.io/gh/mathieugouin/tradesim)
[![CodeFactor](https://www.codefactor.io/repository/github/mathieugouin/tradesim/badge/master)](https://www.codefactor.io/repository/github/mathieugouin/tradesim/overview/master)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mathieugouin_tradesim&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mathieugouin_tradesim)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=mathieugouin_tradesim&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=mathieugouin_tradesim)
![Last Commit](https://img.shields.io/github/last-commit/mathieugouin/tradesim)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview
My ramblings on various stock analysis and data mining.

## Prerequisites
* Python 3.6+
* NumPy (<http://www.numpy.org>)
* SciPy (<http://www.scipy.org>)
* Pandas (<http://pandas.pydata.org/>)
* yfinance (<https://pypi.org/project/yfinance>)

## Quick Start
* If required, edit the stock list files in `stock_db/*.txt`.
* Run (and possibly edit) `download_historical_data.sh` to download the historical stock data locally from the stock list files.
* Run and play with `tradesim.py`

### IPython / Notebook
#### Setup
* `python3 -m pip install --upgrade pip`
* `python3 -m pip install ipython`
* `python3 -m pip install jupyterlab`
* Make sure `~/.local/bin/` is in the path

#### IPython Run
* cd to the current dir where to start
* `ipython`

#### Jupyter Lab Notebook Run
Jupyter lab has a nicer interface.
* cd to the current dir where to start
* `jupyter lab`
* For Github codespace: `jupyter lab --no-browser`

#### Magic command
Ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html
* `%whos`: Print all interactive variables

#### Shortcuts
* `dd`: delete cell
* `a`: insert cell above
* `b`: insert cell below
* `m`: convert cell to markdown (for documentation)
* `y`: convert cell to code (python)
* `Ctrl+Enter`: run current cell
* `Shift+Enter`: run & select cell below
* `Alt+Enter`: run cell & insert below

## Notes
* Sympy equation wrapper: https://raw.githubusercontent.com/mathcube7/customize-sympy/main/customizer.py
