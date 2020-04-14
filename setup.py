import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ksdisc",
    version="0.0.9",
    author="Viktor Wase",
    author_email="viktorwase@gmail.com",
    description="Discrete Kolmogorov–Smirnov test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ViktorWase/ks-disc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)