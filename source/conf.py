# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'memoravel'
copyright = '2024, Pena'
author = 'Pena'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Autodocumentação baseada nas docstrings
    'sphinx.ext.napoleon',     # Suporte a docstrings estilo Google ou NumPy
    'sphinx.ext.viewcode',     # Links para o código fonte
    'sphinx.ext.todo'          # Manter track de todos os TODOs
]

# Adicione esta linha para documentar o conteúdo da classe junto com o __init__
autoclass_content = "both"

templates_path = ['_templates']
exclude_patterns = [
    'build/',             # Diretório de build do Sphinx, onde ele gera a documentação final
    'Thumbs.db',          # Arquivo do Windows
    '.DS_Store',          # Arquivo do macOS
    'memoravel.egg-info/', # Metadados do pacote Python
    '__pycache__/'        # Diretório de cache do Python
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
