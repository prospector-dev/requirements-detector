from distutils.core import setup

comment = 'this is a long comment ' \
          'on two lines'

setup(
    name='prospector-test-1',
    version='0.0.1',
    install_requires=[
        'Django==1.5.0',
        'django-gubbins==1.1.2'
    ]
)