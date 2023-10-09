"""Math utilities library."""

# To make print working for Python2/3
from __future__ import print_function


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Function to test float for approximate equality."""
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
