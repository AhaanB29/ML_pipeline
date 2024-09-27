import sys
from setuptools import setup , find_packages
from typing import List
def req_lst(filename:str)-> List[str]:
    with open(filename) as obj:
        data = obj.readlines()
        data.remove('-e .')
        libs = [a.replace('\n','') for a in data]
    return libs

setup(
    name= 'ML_pipeline',
    version = '0.0.1',
    author='AhaanBanerjee',
    author_email='ahaanbanerjee11@gmail.com',
    requires=req_lst('requirements.txt'),
    packages=find_packages()
)
