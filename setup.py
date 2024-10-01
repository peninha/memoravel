# setup.py

from setuptools import setup, find_packages

setup(
    name="memoravel",
    version="0.1.0",
    description="Uma biblioteca para gerenciar histórico de mensagens, para implementar memória nos Modelos de Linguagem.",
    author="Pena",
    author_email="penadoxo@gmail.com",
    packages=find_packages(),
    install_requires=[
        "tiktoken>=0.1",  # Especifique a versão mínima das dependências
        "jsonschema>=4.0"
    ],
    python_requires=">=3.7",  # Especifique a versão mínima do Python
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
