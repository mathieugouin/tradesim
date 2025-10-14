"""Math utilities library."""


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Function to test float for approximate equality."""
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def step(t):
    """Returns 1 where t >= 0, else 0."""
    return (t >= 0) * 1


def ramp(t):
    """Returns 0 for negative inputs, output equals input for non-negative inputs."""
    return t * step(t)
