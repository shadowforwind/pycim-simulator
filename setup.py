import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycim-simulator",
    version="0.1.0",
    author="peixiangli",
    author_email="peixiangli@quanta.org.cn",
    description="A Python Framework for the Dynamics of Coherent Ising Machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadowforwind/pycim-simulator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7.7",
)
