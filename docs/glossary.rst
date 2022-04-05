:orphan:

.. _glossary:

Glossary
========

.. glossary::

    Compendia
    Compendium
    Compendiums
        A topic is a group of object of interests, it is the composition
        of these subjects.  As an example, suppose you are writing down
        some baking recipes and techniques, the topic here could be *baking*.

        In |project|, a :term:`compendium` is implemented using Sphinx
        :doc:`usage/restructuredtext/domains`.

    Constituent
    Constituents
        Constituents are subject that together make a compendium. As an
        example, suppose you are writing down some baking recipes and
        techniques, the constituents would be *recipes* and *techniques*.

        In |project|, :term:`constituents` are implemented by generating
        :doc:`directives <usage/restructuredtext/directives>` and associated
        :term:`roles`.

        When a constituent is documented, it needs at least one name (its
        :term:`primary name`, optionally :term:`additional names` and some
        content.

    Primary name
    Primary names
        In |project|, documented :term:`constituents` can have many names, but the
        first one is called the :term:`primary name`.  It is used as a
        grouping key in the generated topic :ref:`index <indices>`.

    Alternative names
    Additional names
        When a documented :term:`constituent` have multiple names, those
        that are not the first are :term:`alternative names`. Each additional
        name has its own entry *under* its associated :term:`primary name`
        entry in the generated topic :ref:`index <indices>`. Any name,
        including alternative names, can be used for
        :ref:`cross-referencing <markup>`.

    Role
    Roles
        Roles are often used to cross-reference any documented objects,
        even traversing documentation sites. This means you can use roles
        to cross-reference object *defined in other projects*, thanks to
        the :mod:`sphinx.ext.intersphinx` Sphinx builtin extension.

        See also :term:`roles in the official Sphinx glossary <sphinx:role>`.

        Roles are inline pieces of interpreted text that looks like:

        .. code-block:: rst

            :domain:object_type:`Explicit title <intersphinx_sourcename:qualified_name>`

        Which could be as short as

        .. code-block:: rst

            :object_type:`qualified_name`

        in many cases.

        **domain**
            This would be the domain name, valued ``mytopic``.

            The domain can be made optional by either **locally** (within
            a single document) using the :rst:dir:`default-domain` *directive*
            while the :confval:`primary_domain` *configuration* selects
            a **global** default

        **object_type**
            The Terraform domain defines several objects types (``resource``,
            ``variable``, and more).

            One can also try the :rst:role:`any` role, which might work
            in some cases, yielding an error at build time if the domain
            could not find a matching cross-reference target.

        **Explicit title**
            By default, without having an explicit title the link text
            rendered will be provided by the cross-reference target.
            Put an explicit title to overwrite it. **Without** an explicit
            title, the above example would look like

            .. code-block:: rst

                :domain:object_type:`intersphinx_sourcename:qualified_name`

            Note that the enclosed `` < `` and `` > `` where not necessary
            anymore.

        **intersphinx_sourcename**
            :mod:`sphinx.ext.intersphinx` let us cross-reference objects
            from any third-party documentation.  When two or more
            documentation provide entries for a object of the same name
            and kind, you need to explicitly select the documentation
            source name to which this cross-reference targets. These
            documentation source name are specified by the user as the
            **keys** in the :confval:`intersphinx_mapping` configuration
            dictionary.

            In practice, this is seldom used. **Without** an Intersphinx
            mapping name, the above example would look like

            .. code-block:: rst

                :domain:object_type:`qualified_name`

        **qualified_name**
            The target name of the thing you are cross-referencing to.

        See also:
            Details about roles and cross-references is also covered in
            the :ref:`xref-syntax` section from the official Sphinx docs.

