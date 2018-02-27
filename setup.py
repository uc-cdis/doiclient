from setuptools import setup

setup(
    name='doiclient',
    version='0.1',
    packages=[
        'doiclient',
    ],
    install_requires=[
        'requests>=2.5.2,<3.0.0',
    ],
)
