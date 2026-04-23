"""Sphinx configuration for Auction Assistant docs."""

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

project = "Assistente de Lances"
copyright = "2025, Grupo"
author = "Grupo"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme = "sphinx_rtd_theme"


autodoc_member_order = "bysource"
