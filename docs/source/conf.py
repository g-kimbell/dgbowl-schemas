# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import importlib
import os
import sys
from importlib.metadata import version as get_version

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

# Import all schemas before autodoc adds string annotations
for pkg in ("dgpost", "tomato", "yadg"):
    _ = importlib.import_module(f"dgbowl_schemas.{pkg}").models

version = get_version("dgbowl_schemas")

# -- Project information -----------------------------------------------------

project = "dgbowl-schemas"
copyright = "2022 - 2025, dgbowl authors"
author = "Peter Kraus"
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    # "sphinx.ext.autosummary",
    # "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "body_max_width": "none",
    "sticky_navigation": True,
    "navigation_depth": 6,
}
# html_logo = "./images/yadg.png"
# html_favicon = "./images/yadg_ico.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["images"]


# -- Extension configuration -------------------------------------------------

autosummary_generate = True
autodoc_default_flags = [
    "members",
    "undoc-members",
    "show-inheritance",
]
autodoc_member_order = "bysource"
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_member_order = "bysource"
intersphinx_mapping = {
    "dgpost": ("https://dgbowl.github.io/dgpost/main", None),
    "yadg": ("https://dgbowl.github.io/yadg/main", None),
    "tomato": ("https://dgbowl.github.io/tomato/main", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}
