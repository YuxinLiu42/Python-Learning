import pytest
import sys


@pytest.mark.skipif(sys.version_info < (4, 0), reason="requires python 4")
def test_python_4():
    raise RuntimeError("something went wrong")