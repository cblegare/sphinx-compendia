from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

extras_require = {
    "test": ["nox"],
    "markdown": ["myst_parser", "docutils>=0.16"],
    "docs": [
        "myst_parser",
        "docutils>=0.16",
        "sphinx_autodoc_typehints",
        "sphinx_paramlinks",
        "sphinx_copybutton",
        "sphinxcontrib_bibtex",
        "sphinxcontrib_programoutput",
        "sphinx_tabs",
        "pydata-sphinx-theme",
    ],
}
extras_require["all"] = set(
    dependency
    for extra_dependencies in extras_require.values()
    for dependency in extra_dependencies
)

this_directory = Path(__file__).parent
requirements_in = this_directory.joinpath("requirements.in").resolve()


if __name__ == "__main__":
    setup(
        name="sphinx-compendia",
        version="0.1",
        description="A simple API for creating Sphinx domains and structuring arbitrary collections.",
        long_description=(this_directory / "README.rst").read_text(),
        long_description_content_type="text/x-rst",
        url="https://cblegare.gitlab.io/sphinx-compendia",
        author="Charles Bouchard-Légaré",
        author_email="charlesbouchardlegare@gmail.com",
        license="BSD-2-Clause-Patent",
        project_urls={
            "Documentation": "https://cblegare.gitlab.io/sphinx-compendia",
            "Source": "https://gitlab.com/cblegare/sphinx-compendia",
            "Issue Tracker": "https://gitlab.com/cblegare/sphinx-compendia/-/issues",
        },
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            "Development Status :: 3 - Alpha",
            # Indicate who your project is intended for
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Topic :: Documentation",
            "Topic :: Documentation :: Sphinx",
            "Framework :: Sphinx",
            # Pick your license as you wish (should match "license" above)
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
            "Typing :: Typed",
        ],
        keywords="sphinx",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        python_requires=">=3.7",
        install_requires=requirements_in.read_text().splitlines(),
        extras_require=extras_require,
        entry_points={
            "console_scripts": [],
        },
        include_package_data=True,
    )
