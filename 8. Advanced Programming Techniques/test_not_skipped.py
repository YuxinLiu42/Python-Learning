import pytest
import sys


@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires python 3")
def test_python_3():
    raise RuntimeError("something went wrong")