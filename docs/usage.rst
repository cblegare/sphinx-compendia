.. _usage:

###########
User manual
###########

|project| is very useful to setup what looks like a database of things
we mostly have prose (documentation) about.


.. _use-case:

Example use-case: TTRPG
=======================

Thoughout this guide, we will use the same use case:

    In the context of a *tabletop role-playing game* (TTRPG) such as Pathfinder_
    or `Dungeons and Dragons`_, we are writing an adventure path in a home
    brewed **world** where the story will unfolds.  In order to do this, we will
    need to describe various **locations** and **characters** to our players.

    Also, there are some **house rules** in our game, custom magical **spells**
    and **skills** tailored for our world.

    During game sessions, since the players are the ones who decide what
    happens next, we need to always have our documentation handy, and be
    able to find the right information easily in a few clicks.  By doing
    this, we will be well prepared for improvisation!

This guide takes the form of a walkthough for our specific use-case.
Let's get started!

.. _Pathfinder: https://paizo.com/pathfinder
.. _Dungeons and Dragons: https://dnd.wizards.com/


.. _configuration:

Defining a compendium
=====================

|project| needs to be configured within a Sphinx
:doc:`usage/extensions/index`.  Luckily, we don't need any complex code:
the ``conf.py`` file (:mod:`conf`) itself can be a extension by providing
a ``setup()`` function in it.  This is where we put the definitions of
:term`compendia` and their :term:`constituents`.

At the end of the file, let's add that ``setup()`` function.  This function
takes one parameter: the Sphinx application object.  In this function,
we will use the :func:`sphinx_compendia.make_compendium` function to create
our compendia and register them into Sphinx.

Let's start with our *House rules*:

.. literalinclude:: conf.py
    :language: python
    :linenos:
    :lines: 551-559
    :caption: conf.py

Here is a breakdown of what is happening:

*   On **line 1**, we define the ``setup()`` fonction.  Our ``conf.py``
    becomes a Sphinx extension as required by |project|.

*   On **line 2**, we import the ``make_compendium()`` function, which is
    necessary in order to use it.

*   On **line 6**, we create our topic with its constituents.

    *   The first argument ``"rule"`` is the short name for our topic.
        See details in the :paramref:`sphinx_compendia.make_compendium.name`
        parameter documentation.

    *   The second argument ``"House Rules"`` is a longer, more descriptive
        name for our topic.  See details in the
        :paramref:`sphinx_compendia.make_compendium.display_name` parameter
        documentation.

    *   The third argument ``["skill", "spell"]`` is the list of **consituents**
        of our new topic.  These are the things we are going to be documenting.
        See details in the :paramref:`sphinx_compendia.make_compendium.constituents`
        parameter documentation.

    *   The last argument ``app`` is the Sphinx app.  |project| can register
        itself this way.

That's it! We can now document some house rules.

We will dive into more advanced usages of it in the :ref:`constituent`
section.


.. _markup:

Adding content to a compendium
==============================

As we've seen in :ref:`configuration`, getting started with |project| is
quite simple.

The topic we created made available the :term:`directives <directive>`
``.. rule:skill::`` and ``.. rule:spell::``, as well as the :term:`roles`
``:rule:skill:`` and ``:rule:spell:`` for respectively documenting and
cross-referencing special rules for skills and magic spells.

Let's see it in action:

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst

            .. rule:skill:: coding

                You can write code a computer can understand.

                Writing a small Python script usually requires a result of
                at least **10** on a d20 roll.

            .. rule:spell:: Coder's zone

                When cast, this spell grant the caster the ability to write
                code faster and without bugs, effectively granting a **+10**
                bonus to all :rule:skill:`coding` dice rolls for **30** minutes.

    .. tab:: Result

        .. rule:skill:: coding

            You can write code a computer can understand.

            Writing a small Python script is usually requires a result of
            at least **10** on a d20 roll.

        .. rule:spell:: Coder's zone

            When cast, this spell grant the caster the ability to write
            code faster and without bugs, effectively granting a **+10**
            bonus to all :rule:skill:`coding` dice rolls for **30** minutes.

For each constituent provided in a given topic, a directive is created.
Let's have a closer look using the documentation for a *location*
(the configuration for creating the location constituent is presented
in the :ref:`constituent` section).

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst
            :linenos:

            .. world:location:: Moria
                Khazad-dûm
                Dwarrowdelf

                :world:location:`Khazad-dûm`, commonly known as
                :world:location:`Moria` or the :world:location:`Dwarrowdelf`,
                was an underground kingdom beneath the Misty Mountains.

    .. tab:: Result

        .. world:location:: Moria
            Khazad-dûm
            Dwarrowdelf

            :world:location:`Khazad-dûm`, commonly known as
            :world:location:`Moria` or the :world:location:`Dwarrowdelf`,
            was an underground kingdom beneath the Misty Mountains.

In the example above,

*   On **line 1**, the ``location`` directive from the ``world`` topic is
    used.  ``Moria`` is its first *argument* and becomes this location's
    :term:`primary name`.  The primary name is namely used as a primary
    entry in the :ref:`topic's index <indices>`.

*   On **lines 2 and 3**, :term:`additional names` are given to this location
    as the second and third *arguments* to the directive.

*   On **line 4** we have an empty line, indicating that the directive's
    content follows.  |project| does **not** provide directives with *options*
    yet.  Option names are delimited with ``:`` and must be placed directly
    under *arguments* and above the separating empty line.

*   Starting at **line 5** is the directive's content.  Any valid markup
    can go there, even other |project| directives.  Nested directives have
    some interesting features for some advanced use-cases, as covered in
    the :ref:`nesting` section.  The content block ends as per the normal
    parsing behavior, when a block at a lower indentation level is found.

    The example also shows cross-references to this location using the
    generated :term:`roles`. All of a constituent names (primary or alternate)
    can be used for cross-referencing.

    These roles can be used from anywhere in your documentation.  They
    can even be used other documentation projects using the
    :mod:`sphinx.ext.intersphinx` extension.

.. tip:: When no eligible cross-reference targets are found, |project|
    will not create any link and will emit a **warning**.


.. _default_domain:

Domains, default domain and primary domain
------------------------------------------

Compendia in |project| are implemented using Sphinx
:doc:`usage/restructuredtext/domains`. This is why the compendium's name
(in our example ``rule`` and ``world``) appears in all generated directives
and roles. It can be omited using one of the following methods:

*   The :rst:dir:`default-domain` directive selects a new default domain
    for the rest of a document.

*   The :confval:`primary_domain` configuration value selects a different
    default domain globaly for the whole project.

.. hint:: The primary domain in Sphinx is ``py``, the
    :ref:`Python domain <python-domain>`, by default.

Generated cross-referencing roles can be further shortened.  We will cover
this in the :ref:`following section <constituent>`.

.. _constituent:

More about constituents
=======================

Constituents are what roles and directives are generated for. We can
customize how this happens.  Let's start with an example

    Remember our :ref:`use-case <use-case>`? We also need to document
    **characters** and **locations**.

    Suppose some action scene happens in *Foobartown*, a small city in our
    home brewed fantasy world, one of the various *locations* we will put
    in the documentation.

Let's start with the description of *Foobartown*.

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst

            .. world:location:: Foobartown
                City of Foo Bar

                A nice and cozy town known for its mead industry.

            A cross-reference to :world:location:`Foobartown`.

    .. tab:: Result

        .. world:location:: Foobartown
            City of Foo Bar

            A nice and cozy town known for its mead industry.

        A cross-reference to :world:location:`Foobartown`.


The role ``:world:location:`` is quite long to write and we can shorten
that a bit.  Our constituent was declared with ``loc`` as a cross-referencing
role alias.  We can use both the original and any alias for cross-referencing.

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst

            A cross-reference to :world:loc:`City of Foo Bar`.

    .. tab:: Result

        A cross-reference to :world:loc:`City of Foo Bar`.

We can also add directive aliases the same way:

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst

            .. world:loc:: Plains of Grass

                A green pasture.

    .. tab:: Result

        .. world:loc:: Plains of Grass

            A green pasture.

In order to do this, we used :func:`sphinx_compendia.make_compendium` passing it
:class:`sphinx_compendia.Constituent` instances instead of simple strings for
the :paramref:`sphinx_compendia.make_compendium.constituents` argument.

.. literalinclude:: conf.py
    :language: python
    :linenos:
    :lines: 561-583
    :caption: conf.py

Below is the detailed API documentation for the ``Constituent`` class.
Other things are configurable with this class, namely the whole markup
behavior.  We will cover this in the :ref:`custom-markup` section.


.. _indices:

Indexation
==========

One of the most interesting features of |project| is in its way of providing
an holistic view on a given topic.  It does so by adding all documented
*constituent* and their cross-references to the general index, but also
to a dedicated index.

Each documented *constituent* names and cross-references are put in the
topic index, and are grouped under the constituent's *primary name* index
entry.  The displayed name for cross-references is their *title*.

To generate a link to a topic's index, use the following role markup:

.. code-block:: rst

    :ref:`{topicname}-index`

Here is an example for the *world* topic:

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst

            :ref:`world-index`

    .. tab:: Result

        :ref:`world-index`

This can be customized using the :paramref:`sphinx_compendia.make_compendium.index_name`
parameter.

.. warning:: There is a known performance issue in the generation of
    |project| compendium indices.  This issue should not be too grim unless
    you are working with a very large compendium scattered in numerous
    documentation files.  See :ref:`known-issues` for details.


 .. _search-results:

Nice search results
-------------------

|project| feeds Sphinx the information it expects for relevant search result,
using the localized topic's display name and constituent type name.

For instance, the :world:location:`Moria` above as a search result would
be described as "*Some Mythical World location*".
