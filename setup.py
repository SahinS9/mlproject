# it will help to build this ml project as the package so with the setup.py 3rd party will be able to use it


from setuptools import find_packages, setup
from typing import List

#not feasible to write all 100s of packages in the list so will use this function


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str) -> List[str]:
    """
    this function will return list of requirements
    """

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

        # -e . should not get considered in requirements

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name = "mlproject",
    version = '0.0.1',
    author = "ss",
    author_email="shahinsaatov@gmail.com",
    packages = find_packages(),
    # install_requires = ['pandas','numpy','seaborn'],
    install_requires = get_requirements('requirements.txt'),
    
)