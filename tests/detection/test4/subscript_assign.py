"""
This test is to verify that top level subscript assigns (x[y]) don't break the
parser. For version <=0.1, a subscript assign would break the setup.py AST walker
completely.
"""

from distutils.core import setup

something = dict()
something["fish"] = ["a", "b", "c"]

setup(name="prospector-test-1", version="0.0.1", install_requires=("Django==1.5.0", "django-gubbins==1.1.2"))
