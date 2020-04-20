import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "example-pkg-naudeconradie",
    version = "0.0.1",
    author = "Naudé Conradie",
    author_email = "naudeconradie@gmail.com",
    description = "An example package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 1 - Planning",
        "Environment :: Other Environment",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
    ],
    python_requires = "==3.6"
)