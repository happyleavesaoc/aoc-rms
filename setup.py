from setuptools import setup, find_packages

setup(
    name='aoc-rms',
    version='1.0.0',
    description='Age of Empires 2 RMS utilities',
    url='https://github.com/happyleavesaoc/aoc-rms/',
    license='MIT',
    author='happyleaves',
    author_email='happyleaves.tfr@gmail.com',
    packages=find_packages(),
    install_requires=['numpy', 'pyparsing', 'scipy', 'sklearn'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
