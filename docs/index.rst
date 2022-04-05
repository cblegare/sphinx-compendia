#########
|project|
#########

.. container:: tagline

    A simple API for creating Sphinx_ domains_ and structuring arbitrary
    collections.

|project| is especially useful for documenting **collections**, **compendiums**,
**catalogs**, **inventories**, **compilations**, **digests** and such.
You can find a few :ref:`example use cases <use-cases>` below.

    We write documentation to communicate efficiently complex topics.
    |project| help see how the constituents of a topic are linked together
    **and** have a holistic view of what matters.

|project| helps you leverage the best feature from Sphinx_ for the compendia
that are meaningful for *you* and your **readers**.

*   Integrates nicely in your existing workflow. See :ref:`configuration`.

*   Powerful **cross-referencing** capabilities, even between separate
    documentation projects.  Keeping links with URLs up-to-date is **hard**,
    cross-referencing with |project| saves you time.  See :ref:`markup`.

*   Compendium-specific **indices** so you can browse all your documented
    constituent at a glance, so readers can take a step back and browse
    your compendia as a **whole**.  See :ref:`indices`.

*   Efficient **search** in built web sites.  See :ref:`search-results`.

*   Works for any reading **medium** Sphinx supports, from HTML pages to
    eReaders.

*   While **simple by default**, |project| is also **extensible**!
    See :ref:`custom-markup`.

|project| is named after its main use-case: compendiums.  The word *compendia*
is another plural form of *compendium*.  We use both plural forms in this
documentation.

.. _quickstart:

Quickstart
==========

*   :ref:`Install <installation>` |project|
*   :ref:`Define a topic and some constituents <configuration>` as an
    extension in your ``conf.py`` file (:mod:`conf`)

    .. code-block:: python

        from sphinx_compendia import make_compendium

        def setup(app):
            # Provide a topic shortname and some constituents
            make_compendium("baking", ["recipe", "technique"], app=app)

*   :ref:`Use the generated directives and roles <markup>`, in this case
    ``.. baking:recipe::``, ``.. baking:technique::``, ``:baking:recipe:``
    and ``:backing:technique:``.
*   :ref:`Browse the generated index <indices>`


.. _use-cases:

Example use-cases
=================

Writing a **table-top roleplaying game** adventure path *as code*
    *We will use this use case in our examples.*

    we are writing an adventure path in a home brewed world named Fjordlynn
    for some table top role-playing game. We want to document characters
    and locations along with some house rules for skills and magic spells.

    We will create two compendia: ``world`` and ``rule`` for respectively
    documenting ``character`` and ``location``, and ``skill`` and ``spell``,
    generating automatically the required directives and cross-referencing
    roles.

Creating a **user experience** design system *as code*
    Document a UX topic with *personas*, *markets* or other interesting
    constituents.  Cross-reference these from your BDD_ specifications
    documented with Sphinx-Gherkin_!

Building **IT management** systems *as code*
    Document *teams*, *services*, *assets* and *configuration items* for
    your ITIL_ (or other IT management framework) documentation.

**Cookbook** *as code*
    Publish your best *meatloaf* and *kimchi* recipes with style.  You can
    even use |project| for a printed book!


.. _installation:

Installation
============

Install |project|:

.. code-block:: shell

    pip install -U sphinx-compendia


Get started
===========

.. tip:: Get started in no time, go to our :ref:`usage` section!


.. toctree::
    :maxdepth: 1
    :hidden:

    usage
    advanced
    contributing
    changelog
    about


.. _links:

Links
=====

|project| is

- `Hosted on Gitlab <https://gitlab.com/cblegare/sphinx-compendia>`__
- `Mirrored on Github <https://github.com/cblegare/sphinx-compendia>`__
- `Distributed on PyPI <https://pypi.org/project/sphinx-compendia/>`__
- `Documented online <https://cblegare.gitlab.io/sphinx-compendia/>`__


Indices and references
======================

*   :ref:`genindex`
*   :ref:`search`
*   :ref:`glossary`


.. _BDD: https://en.wikipedia.org/wiki/Behavior-driven_development
.. _domains: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
.. _Sphinx-Gherkin: https://cblegare.gitlab.io/sphinx-gherkin/
.. _ITIL: https://en.wikipedia.org/wiki/ITIL
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
