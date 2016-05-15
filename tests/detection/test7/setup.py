# -*- coding: UTF-8 -*-
from distutils.core import setup

if foo:
    # just for a test with indentation
    bar()

setup(
    name=u'prospector-test-4-üéø',
    version='0.0.1',
    install_requires=[
        'Django==1.5.0',
        'django-gubbins==1.1.2'
    ]
)
