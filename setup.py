from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def getRequirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

        return requirements


setup(
    name= 'DiamondPricePredection',
    varsion = '0.0.1',
    author = 'Aryan Dhirhi',
    install_requires = getRequirements('requirements.txt'),
    packages=find_packages()
)