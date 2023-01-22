from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ndl_aspect", # the name of the project. It's what's used for "pip install xxxx"
    version="0.0.1", # Each time you upload an update, you need to update this number
    license = 'MIT',
    author="Irene Testini",
    description="A package for training NDL models to predict aspect in Polish verbs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    download_url= "https://github.com/ooominds/Polish-Aspect/archive/refs/tags/v_01.tar.gz",
    keywords=["NDL", "NLP", "Polish", "Aspect"],
    install_requires=[
        'numpy',
        'h5py',
        'pandas',
        'pyndl',
        'sklearn',
        'keras',
        'xarray',
        'matplotlib',
        'nltk'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["ndl_aspect"],
)