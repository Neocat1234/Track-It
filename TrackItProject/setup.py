from setuptools import setup, find_packages

setup(
    name='17TrackInfoExtract',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here if any
    ],
    author='Vansh Parekh',
    description='This project is built to extract information on pacakages from 17 Track API's',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Neocat1234',
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add more classifiers as needed
    ],
)
