# setup.py

from setuptools import setup, find_packages

setup(
    name="memoravel",
    version="0.1.1",
    description="A library to manage message history, for implementing memory in Language Models.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Pena",
    author_email="penadoxo@gmail.com",
    url='https://github.com/peninha/memoravel',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "tiktoken>=0.1",
        "jsonschema>=4.0"
    ],
    keywords='LLM memory message history',
    license='MIT',
)
