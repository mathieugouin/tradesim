"""
This simple module allows importing module from parent directory.
It adds the parent directory of this file to the sys.path.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
