import sys
import re

def test_platform():
    assert re.search("\d", sys.platform)

def test_replace():
    assert "".replace("", "A", 2) == "A"

