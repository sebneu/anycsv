from setuptools import setup, find_packages

setup(
    name='anycsv',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'file-magic',
        'cchardet'
    ],
    url='https://github.com/sebneu/anycsv',
    license='',
    author='Sebastian Neumaier',
    author_email='',
    description='A robust CSV parser.'
)
