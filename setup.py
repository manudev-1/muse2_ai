from setuptools import setup, find_packages

with open('requirements.txt', "r") as f:
    required = f.read().splitlines()

setup(
    name="Muse2_ai",
    version="0.0",
    packages=find_packages(),
    install_requires = required,
    entry_points = {
      'console_scripts': [
            #! "cmd=module.file:start_function"
      ]  
    },
    
    author="Manuele Barone",
    author_email="manuelebarone186@gmail.com",
    description="Personal project from EEG interpretation to Image",
    long_description=open("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/manudev-1/muse2_ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)