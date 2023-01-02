# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os.path

sys.path.insert(0, os.path.abspath("../../src"))

project = "Sneks"
copyright = "2023, Nathaniel Schaaf"
author = "Nathaniel Schaaf"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "myst_parser",
]
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = ["node_modules"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 5, "titles_only": True}
html_static_path = ["_static"]
