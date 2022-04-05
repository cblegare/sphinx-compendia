.. _advanced:

##############
Advanced usage
##############

|project| is already flexible enough for some more advanced usage. This
document explains a few of them.


.. _nesting:

Nesting constituents
====================

You can use constituent directives from within other constituent directives.
In conjunction with :term:`primary names` and :term:`alternative names`,
this can provide interesting results, including having the same names in
multiple constituents.

    Remember our :ref:`example use-case <use-case>` to document a fantasy
    world?

    Let's add a criminal organisation, the *Golden Retrievers*, a nefarious
    group of burglars and cutpurses.  They have branches in various cities,
    but their headquarter lies in the metropolis of *Adenaginia*.

Let's document the metropolis and the *Golden Retrievers* headquarter.

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst
            :linenos:

            .. world:location:: Adenaginia

                A very big city.

                .. world:location:: Golden Keep
                    Golden Retrievers Headquarters
                    Golden Retrievers branch

                    A small keep most honest people avoid since it is the
                    *Golden Retrievers'* headquarters.

            * Cross-reference to :world:loc:`Reeky Lunch`
            * Cross-reference to :world:loc:`Adenaginia.Golden Retrievers branch`

    .. tab:: Result

        .. world:location:: Adenaginia

            A very big city.

            .. world:location:: Golden Keep
                Golden Retrievers Headquarters
                Golden Retrievers branch

                A small keep most honest people avoid since it is the
                *Golden Retrievers'* headquarters.

        * Cross-reference to :world:loc:`Golden Keep`
        * Cross-reference to :world:loc:`Adenaginia.Golden Retrievers branch`

Nesting constituent makes it possible to specify a cross-reference target
with the parent names.  In the above example, the cross-reference
``:world:loc:`Adenaginia.Golden Retrievers branch``` include a parent
constituent name.

Now, let's document a small fishing village where the *Golden Retrievers*
also make business. We will see that two ``Golden Retrievers branch``
can be cross-referenced independently.

.. tabs::

    .. tab:: Markup code

        .. code-block:: rst
            :linenos:

            .. world:location:: Maarbridge

                A very small fishing village.
                Farmers avoid its :world:loc:`shady inn <.Golden Retrievers branch>`.

                .. world:location:: Reeky Lunch
                    Golden Retrievers branch

                    A tavern where the food stinks.  It is known to be
                    controlled by the *Golden Retrievers* criminal group.

                .. world:location:: Maar Manor
                    Town Hall

                    Where the mayor lives.
                    It is far from :world:loc:`.Golden Retrievers branch`

            * Cross-reference to :world:loc:`Maarbridge.Golden Retrievers branch`

    .. tab:: Result

        .. world:location:: Maarbridge

            A very small fishing village.
            Farmers avoid its :world:loc:`shady inn <.Golden Retrievers branch>`.

            .. world:location:: Reeky Lunch
                Golden Retrievers branch

                A tavern where the food stinks.  It is known to be
                controlled by the *Golden Retrievers* criminal group.

            .. world:location:: Maar Manor
                Town Hall

                Where the mayor lives.

        * Cross-reference to :world:loc:`Maarbridge.Golden Retrievers branch`


By providing explicitely the parent's name in the cross-reference role,
we can make sure that the right constituent is linked.

Also, on **line 4**, we have omitted the parent's name but kept a leading
dot (``.``) to indicate that this cross-reference target is **relative**
to the current nesting position.

.. tip:: When multiple eligible cross-reference targets are found, |project|
    will link to the **first one** and will emit a **warning**.


.. _admissible-nesting:

Restricting admissible nesting
------------------------------

It is possible to restrict the cross-reference search to specific constituent
types. As an example, we could forbid to look for **spell** parents when
cross-referencing a **skill**, or simply disable cross-referencing with
a parent namespace. See
:paramref:`admissible_parent_objtypes <sphinx_compendia.Constituent.admissible_parent_objtypes>`
for details.


.. _custom-markup:

Advanced customization
======================

You can provide your own directive and role implementation to respectively
the :paramref:`directive_class <sphinx_compendia.Constituent.directive_class>`
and :paramref:`xrefrole_class <sphinx_compendia.Constituent.xrefrole_class>`
arguments to the :class:`sphinx_compendia.Constituent` constructor. The safer
methods to override are used to change how directives and cross-references
are displayed.  The API documentation below gives more details.

.. autoclass:: sphinx_compendia.markup.ConstituentDescription
    :members:

.. autoclass:: sphinx_compendia.markup.ConstituentReference
    :members:


.. _constituent-api:

Constituents details
====================

Below is the complete API documentation for configuring constituents.

.. autoclass:: sphinx_compendia.Constituent


Even deeper customization
=========================

.. autofunction:: sphinx_compendia.make_compendium


.. _custom-index:

Customizing the topic index
---------------------------

.. danger:: Unstable API ahead

.. autoclass:: sphinx_compendia.index.Index
    :members:


.. _custom-domain:

Customizing the domain
----------------------

.. danger:: Don't try it **at all**.

.. autoclass:: sphinx_compendia.domain.Domain
    :members:
