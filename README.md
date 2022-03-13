# Trading Simulator
[![Python Build](https://github.com/mathieugouin/tradesim/actions/workflows/ci.yml/badge.svg)](https://github.com/mathieugouin/tradesim/actions/workflows/ci.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/mathieugouin/tradesim/badge/master)](https://www.codefactor.io/repository/github/mathieugouin/tradesim/overview/master)
[![codecov](https://codecov.io/gh/mathieugouin/tradesim/branch/master/graph/badge.svg?token=4ZZ9V7NU91)](https://codecov.io/gh/mathieugouin/tradesim)
![Last Commit](https://img.shields.io/github/last-commit/mathieugouin/tradesim)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview
My ramblings on various stock analysis and data mining.

## Prerequisites
* Python 2.7
* NumPy (<http://www.numpy.org>)
* SciPy (<http://www.scipy.org>)
* Pandas (<http://pandas.pydata.org/>)
* yfinance (<https://pypi.org/project/yfinance>)
* mpl_finance (<https://github.com/matplotlib/mpl_finance>)

## Quick Start
* If required, edit the stock list files in `stock_db/*.txt`.
* Run (and possibly edit) `download_historical_data.sh` to download the historical stock data locally from the stock list files.
* Run and play with `tradesim.py`

## Project notes
* Histogram plot of data: <http://stackoverflow.com/questions/5328556/histogram-matplotlib/5328669>

### IPython
Setup:
* `python3 -m pip install --upgrade pip`
* `python3 -m pip install ipykernel`
* `python3 -m pip install jupyter`

Run:
* cd to the current dir where to start
* `jupyter notebook`
* Or to directly open a notebook: `jupyter notebook tradesim_notebook.ipynb`

Shortcuts:
* dd: delete cell
* a: insert cell above
* b: insert cell below
* m: convert cell to markdown (for documentation)
* y: convert cell to code (python)
* shift+enter: run & select cell below

## Project TODO
* Analyze invalid stock
* Cleanup ticker files
