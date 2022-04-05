.. _about:

#####
About
#####

.. _rationale:

Why |project| was written?
==========================

Structuring a compendium and tracking cross-references has always been a
challenge for a couple of personal projects, namely cooking recipes and
tabletop role-playing game redaction.  After I wrote a few Sphinx extensions
(Sphinx-Terraform_ and Sphinx-Gherkin_), I had finally enough knowledge
of the Sphinx API to find a solution.

.. _Sphinx-Terraform: https://cblegare.gitlab.io/sphinx-terraform/
.. _Sphinx-Gherkin: https://cblegare.gitlab.io/sphinx-gherkin/


.. _known-issues:

Known issues
============

Cross-references in a domain index is suboptimal
------------------------------------------------

Since domain indices are computed *before* cross-references are resolved
in, we have to rebuild the indices for each document as a post-transform
step.  Solutions are investigated directly in Sphinx.  See the following
issues:

*   https://github.com/sphinx-doc/sphinx/issues/10299
*   https://github.com/sphinx-doc/sphinx/issues/10295

The post-transform is performed by the following class.

.. autoclass:: sphinx_compendia.domain.BackrefsIndexer
    :members: run


.. _license:

License
=======

|project|

Copyright © 2022  Charles Bouchard-Légaré


.. literalinclude:: ../LICENSE
    :language: none
