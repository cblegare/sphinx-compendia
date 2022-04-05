from __future__ import annotations

from typing import Any, Generic, List, Optional, Tuple, TypeVar

from docutils import nodes
from docutils.nodes import Element, Node, system_message
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_id

from sphinx_compendia import SphinxCompendiaError
from sphinx_compendia.domain import Domain
from sphinx_compendia.sphinxapi import SphinxGeneralIndexEntry


class ConstituentDescription(ObjectDescription[str]):
    """
    Capture the definition of a constituent within a directive.

    An constituent can have more than one name, all of which can be used
    for cross referencing.

    Example:
        Given the directive's name is ``character`` within the ``world``
        domain,

        .. code-block:: rst

            .. world:character:: Gardakan
                Lord Gardakan
                Gardy

                A mighty paladin!

        This character will

        *   Be available for cross referencing with the ``:world:character:``
            role (see :class:`~ConstituentReference`)

        *   Be listed in the ``world`` domain index
            (see :class:`sphinx_compendia.index.Index`)

        *   Be listed in the general index.
    """

    has_content = True
    required_arguments = 1

    constituent_objtype: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.namespace: RefContextStack[str] = RefContextStack(
            self.env, "namespace"
        )

    def handle_signature(
        self, sig: str, signode: addnodes.desc_signature
    ) -> str:
        """
        Parse the signature into nodes and append them to the signature node.

        More specifically, ``handle_signature`` implements parsing the
        signatures of the directive and passes on the constituent’s name
        and type to its superclass while providing the nodes used for
        displaying the signatures (names).

        For instance, given the following directive definition

        .. code-block:: rst

            .. world:character:: Guy McMaskface
                Guy McFace

                Some description of Guy.

        then ``Guy McMaskface`` and ``Guy McFace`` will be passed as the
        `sig` parameter in subsequent calls.

        .. hint:: Subclasses should consider re-implementing this method
            with caution.  Consider overriding

            *   :meth:`~make_primary_signature_nodes`
            *   :meth:`~make_secondary_signature_nodes`

            instead.

        Args:
            sig:
                The signature, ``Guy McMaskface`` from the the example above.
            signode:
                The signature document node.  It acts like the `term` part
                of a glossary entry.

                Given the example above, then the signode is a RestructuredText
                node that will be extended to represented with the following
                pseudo-HTML:

                .. code-block:: html

                    <dl class="world character">
                      <dt id="world-chracter-Guy-McMaskface">
                        Guy McMaskface
                      </dt>
                      <dt id="world-character-Guy-McFace">
                        Guy Mcface
                      </dt>
                      <dd>
                        <p>
                          Some description of Guy.
                        </p>
                      </dd>
                    </dl>

        Returns:
            We return a nice unique url friendly anchor name.

            The return value should be a value that identifies the constituent.
            It is passed to :meth:`add_target_and_index()` unchanged,
            and otherwise only used to skip duplicates.
        """
        identifier = make_id(self.env, self.state.document, self.name, sig)

        if not self.names:
            signode.extend(self.make_primary_signature_nodes(sig))
            self.namespace.push(sig)
        else:
            signode.extend(self.make_secondary_signature_nodes(sig))

        return identifier

    def after_content(self) -> None:
        self.namespace.pop()

    def make_primary_signature_nodes(self, sig: str) -> List[nodes.Element]:
        """
        Generate the appropriate nodes for rendering the primary name signature.

        Args:
            sig: The signature as a string.

        Returns:
            Docutils node for displaying the primary name signature.
        """
        localized_objtype = (
            self.get_topic_domain().object_types[self.objtype].lname.title()
        )

        return [
            addnodes.desc_annotation(
                self.objtype,
                "",
                nodes.Text(localized_objtype),
            ),
            addnodes.desc_sig_space(),
            addnodes.desc_name(text=sig),
        ]

    def make_secondary_signature_nodes(self, sig: str) -> List[nodes.Element]:
        """
        Generate the appropriate nodes for rendering the other name signatures.

        Args:
            sig: The signature as a string.

        Returns:
            Docutils node for displaying the alternate name signatures.
        """
        return [
            addnodes.desc_sig_punctuation(
                "—",
                "—",
            ),
            addnodes.desc_sig_space(),
            addnodes.desc_name(text=sig),
        ]

    def add_target_and_index(
        self, anchor: str, sig: str, signode: addnodes.desc_signature
    ) -> None:
        """
        Add cross-reference IDs and entries to indices, if applicable.

        This method will add this character name to the domain database
        (hence to the domain index) and to the general index.

        .. hint:: Subclasses should consider re-implementing this method
            with caution since it is responsible for registering this
            constituent's description to the domain data, and this API is
            not stable yet.

        Example:
            Using the following usages of this directive

            .. code-block:: rst

                .. world:character:: Guy McMaskface
                    Guy McFace

                    Some description of Guy.

                .. world:location:: Docktown

                    Some description of the city of Docktown.

            This method would be called once per signature, which means
            three (3) times, on two separate instances, the one named
            ``character`` and the one named ``location``.

        Args:
            anchor:
                The identifying name of this character name as returned by
                :meth:`~handle_signature`.  This name can act as a valid
                URL fragment (after the ``#`` part), an anchor, unique
                within a document.
            sig:
                One signature, which is the object name we are indexing.

                In the above example, both ``Guy McFace`` and
                ``Guy McMaskface``  will be passed
                as the `sig` parameter in separate invocations.
            signode:
                The signature document node as generated in
                :meth:`~handle_signature`.
        """
        # Not exactly sure how this works
        signode["ids"].append(anchor)
        self.state.document.note_explicit_target(signode)

        # First, register this object to the domain
        self.note_constituent_signature(anchor, sig, signode)
        # Then, add index entries for it
        generalindex_entry = SphinxGeneralIndexEntry(
            entrytype="single",
            entryname=sig,
            targetid=anchor,
            mainname=sig,
            key=None,
        )
        inode = addnodes.index(entries=[generalindex_entry])
        self.indexnode.append(inode)

    def get_topic_domain(self) -> Domain:
        """
        Get the underlying domain for this constituent's topic.

        Returns:
            Type-hinted domain.
        """
        return self.env.domains[self.domain]  # type: ignore

    def note_constituent_signature(
        self, anchor: str, signature: str, signode: addnodes.desc_signature
    ) -> None:
        domain = self.get_topic_domain()

        object_id = self.names[0]
        objtype = self.objtype

        return domain.note_constituent_signature(
            objtype,
            self.name,
            object_id,
            anchor,
            signature,
            self.namespace.stack,
            signode,
        )

    @property  # type: ignore
    def objtype(self) -> str:  # type: ignore
        """
        The objtype for documented constituents for this directive.

        The parent class behavior is to set this property based on the
        directive name.  In order to enable the possibility to have
        different directive names creating the same objtype, we override
        this property to have it always return the same objtype disregarding
        the directive name.  In other words, setting this property is a
        no op, does nothing.

        Returns:
            The objtype for documented constituent with this directive.
        """
        return self.constituent_objtype

    @objtype.setter
    def objtype(self, value: Any) -> None:
        pass


class ConstituentReference(XRefRole):
    """
    Define a constistuent reference role.

    These references are added to the general index.
    """

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> Tuple[str, str]:
        """
        Process link for a given cross-reference role.

        See also:
            The parent class method docstring is something like

                Called after parsing title and target text, and creating
                the reference node (given in *refnode*).  This method can
                alter the reference node and must return a new (or the same)
                ``(title, target)`` tuple.
        Args:
            env:
                Sphinx build environment.
            refnode:
                The created referenced node, which can be altered here.
            has_explicit_title:
                An explicit title in a role is when a display string is
                provided as part of the role's interpreted text. For example

                .. code-block: rst

                    :ref:`Here is an explicit title<some-reference-target>`

                would diplay an hyperlink to ``some-reference-target`` with
                ``Here is an explicit title`` as the link text.

                This value is also available as a instance member with the
                same name (``self.has_explicit_title``).
            title:
                The link title.
            target:
                The link target identifier.

        Returns:
            Title and target strings.
        """
        title, target = super().process_link(
            env, refnode, has_explicit_title, title, target
        )
        namespace: RefContextStack[str] = RefContextStack(env, "namespace")

        if target.startswith("."):
            newtarget = ".".join(
                part for part in [".".join(namespace.stack), target[1:]] if part
            )
            if target.endswith("."):
                newtarget += "."
            target = newtarget

        return title, target

    def result_nodes(
        self,
        document: nodes.document,
        env: BuildEnvironment,
        node: Element,
        is_ref: bool,
    ) -> Tuple[List[Node], List[system_message]]:
        """
        Add general index nodes just before returning the finished xref nodes.

        .. hint:: Subclasses should consider re-implementing this method
            with caution since it is responsible for registering this
            constituent's cross-reference to the domain data, and this API
            is not stable yet.

        Args:
            document: Source document where this ref was defined.
            env: Current Sphinx build environment.
            node: This role's node.
            is_ref: True when this is the reference node, else it's the
                content node.

        Returns:
            Not sure what the second item of this tuple should be.
        """
        anchor = make_id(
            self.env, document, "sphinx_compendia#backrefs", self.rawtext
        )
        node["ids"].append(anchor)
        document.set_id(node)
        self._note_general_index(node)
        return [node], []

    def _note_general_index(self, node: Element) -> None:
        entry = SphinxGeneralIndexEntry(
            entrytype="single",
            entryname=self.target,
            targetid=node["ids"][0],  # targetid=self.rawtext,
            mainname=node.attributes.get("refdoc", ""),
            key=None,
        )
        inode = addnodes.index(entries=[entry])
        node.append(inode)


T = TypeVar("T")


class RefContextStack(Generic[T]):
    def __init__(self, env: BuildEnvironment, key: str):
        """
        Provide a stack-like data structure in the build environment.

        The idea behind this is to share some data between directives and
        role implementations.  We use a stack to help support implementations
        that enable specific features when directives are nested within
        each other.

        Examples:
            >>> class StubEnvironment:
            ...     ref_context = {}
            >>> env = StubEnvironment()
            >>> namespace: RefContextStack[str] = RefContextStack(env, "namespace")
            >>> namespace.stack
            []
            >>> namespace.push("foo")
            >>> namespace.stack
            ['foo']
            >>> namespace.push("bar")
            >>> namespace.stack
            ['foo', 'bar']
            >>> namespace.peek()
            'bar'
            >>> namespace.stack
            ['foo', 'bar']
            >>> namespace.pop()
            'bar'
            >>> namespace.stack
            ['foo']
            >>> namespace.pop()
            'foo'
            >>> None == namespace.pop()
            True

        Args:
            env:
                The build environment is the container for this reference
                context stack.
            key:
                We store our stack under a certain key.
        """
        self.env = env
        self.key = key

    @property
    def stack(self) -> List[T]:
        stack = self.env.ref_context.setdefault(self.key, [])
        if isinstance(stack, list):
            return stack
        else:
            raise SphinxCompendiaError(
                f"ref_context for '{self.key}' was of unexpected "
                f"type '{type(stack)}'."
            )

    def push(self, value: T) -> None:
        self.stack.append(value)

    def peek(self) -> Optional[T]:
        if self.stack:
            return self.stack[-1]
        else:
            return None

    def pop(self) -> Optional[T]:
        try:
            return self.stack.pop()
        except IndexError:
            return None
