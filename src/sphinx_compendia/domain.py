from __future__ import annotations

import sys
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
)

from docutils.nodes import Element, Node
from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain as _Domain
from sphinx.domains import Index, IndexEntry
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.transforms.post_transforms import (
    ReferencesResolver,
    SphinxPostTransform,
)
from sphinx.util.logging import getLogger
from sphinx.util.nodes import make_refnode

from sphinx_compendia.i18n import t__
from sphinx_compendia.sphinxapi import SphinxDomainObjectDescription
from sphinx_compendia.store import CompendiumData, CompendiumObject, Ref

if TYPE_CHECKING or sys.version_info < (3, 8, 0):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

log = getLogger(__name__)


D = TypeVar("D", bound="Domain")


class DomainData(TypedDict, total=False):
    version: int
    topic_data: CompendiumData


class Domain(_Domain):
    """
    A Sphinx domain is a specialized container that ties together
    roles, directives, and indices, among other things.
    """

    name: str
    label: str
    roles: Dict[str, XRefRole]  # type: ignore
    directives: Dict[str, Type[ObjectDescription[str]]]
    indices: List[Type[Index]]
    initial_data: DomainData  # type: ignore

    @classmethod
    def make_initial_data(
        cls,
        objtypes: Iterable[str],
        admissible_parent_objtypes: Dict[str, Set[str]],
    ) -> DomainData:
        return dict(
            topic_data=CompendiumData.initial_data(
                objtypes, admissible_parent_objtypes
            )
        )

    @property
    def _store(self) -> CompendiumData:
        return self.data["topic_data"]  # type: ignore

    def note_constituent_signature(
        self,
        objtype: str,
        objtype_alias: str,
        object_id: str,
        anchor: str,
        signature: str,
        namespace: List[str],
        signode: addnodes.desc_signature,
    ) -> None:
        object_description = SphinxDomainObjectDescription(
            anchor,
            signature,
            objtype,
            self.env.docname,
            anchor,
            1,
        )
        self._store.add_object(
            objtype,
            objtype_alias,
            object_id,
            object_description,
            namespace,
            signode,
        )

    def get_compendium_objects(
        self, docnames: Optional[List[str]] = None
    ) -> Dict[CompendiumObject, List[SphinxDomainObjectDescription]]:
        result = {}
        for compendium_object in self._store.compendium_objects.values():
            object_descriptions = self._store.object_descriptions[
                compendium_object.object_id
            ]
            if docnames is not None:
                result[compendium_object] = [
                    object_description
                    for object_description in object_descriptions
                    if object_description.docname in docnames
                ]
            else:
                result[compendium_object] = self._store.object_descriptions[
                    compendium_object.object_id
                ]
        return result

    def get_refs(
        self, object_description: SphinxDomainObjectDescription
    ) -> List[Ref]:
        return self._store.signature_references[object_description]

    def get_objects(self) -> Iterable[SphinxDomainObjectDescription]:
        """
        Return an iterable of "object descriptions".

        See Also:
             Parent method :meth:`sphinx.domains.Domain.get_objects`.

        Returns:
            Object descriptions are tuples with six items.
            See :class:`.sphinxapi.SphinxDomainObjectDescription`.
        """
        yield from self._store.find_object_descriptions()

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        reference_type: str,
        target: str,
        node: addnodes.pending_xref,
        contnode: Element,
    ) -> Optional[Element]:
        """
        Resolve the pending_xref *node* with the given *reference_type* and *target*.

        Args:
            env:
                Current Sphinx build environment.
            fromdocname:
                Document name where the cross-reference was used.
            builder:
                Current Sphinx builder.
            reference_type:
                Reference type name. Basically, the reference role name.
            target:
                Looked up object identifier.
            node:
                Document node for the xref.
            contnode:
                The markup content of the cross-reference.

        If no resolution can be found, ``None`` can be returned;
        the xref node will then given to the ``missing-reference`` event,
        and if that yields no resolution, replaced by contnode.

        Returns:
            A reference node or None if no reference could be resolved.
        """
        resolved = self._resolve_xref(target, reference_type)

        if not resolved:
            return None

        if len(resolved) > 1:
            candidates = " or ".join(
                f":{self._make_rolename(object_description)}:`{target}`"
                for _, object_description in resolved
            )
            log.warning(
                t__(
                    "more than one target found for '%s' cross-reference %r: could be %s"
                ),
                reference_type,
                target,
                candidates,
                location=node,
            )

        compendium_object, object_description = resolved[0]
        refnode = self._make_refnode(
            builder, contnode, fromdocname, object_description
        )
        self._backref_xref(node, object_description)
        return refnode

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: addnodes.pending_xref,
        contnode: Element,
    ) -> List[Tuple[str, Element]]:
        """
        Resolve the pending_xref *node* with the given *target*.

        Args:
            env:
                Current Sphinx build environment.
            fromdocname:
                Document name where the cross-reference was used.
            builder:
                Current Sphinx builder.
            target:
                Looked up object identifier.
            node:
                Document node for the xref.
            contnode:
                The markup content of the cross-reference.

        Returns:
            The method must return a list (potentially empty) of tuples
            ``("domain:role", newnode)``, where ``"domain:role"`` is the
            name of a role that could have created the same reference,
            e.g. ``'py:func'``. ``newnode`` is what :meth:`resolve_xref`
            would return.
        """
        result = [
            (
                self._make_rolename(object_description),
                self._make_refnode(
                    builder, contnode, fromdocname, object_description
                ),
            )
            for _, object_description in self._resolve_xref(target)
        ]

        return result

    def _backref_xref(
        self,
        node: addnodes.pending_xref,
        object_description: SphinxDomainObjectDescription,
    ) -> None:
        self._store.add_backref(
            object_description, self.env.docname, node["ids"][0], node.astext()
        )

    def _resolve_xref(
        self,
        target: str,
        reference_type: Optional[str] = None,
    ) -> List[Tuple[CompendiumObject, SphinxDomainObjectDescription]]:
        try:
            objtypes = (
                self.objtypes_for_role(reference_type)
                if reference_type
                else self.object_types.keys()
            )
            return list(self._store.find(objtypes, target))
        except KeyError:
            return []

    def _make_refnode(
        self,
        builder: Builder,
        contnode: Node,
        fromdocname: str,
        obj_description: SphinxDomainObjectDescription,
    ) -> Element:
        new_node = make_refnode(
            builder,
            fromdocname,
            obj_description.docname,
            obj_description.anchor,
            contnode,
            obj_description.dispname,
        )
        return new_node

    def _make_rolename(
        self, object_description: SphinxDomainObjectDescription
    ) -> str:
        role_name = (
            f"{self.name}:{self.role_for_objtype(object_description.type)}"
        )
        return role_name


class BackrefsIndexer(SphinxPostTransform):
    default_priority = ReferencesResolver.default_priority + 1

    index_class: Type[Index]
    domain_name: str

    def is_supported(self) -> bool:
        return super().is_supported() and hasattr(
            self.app.builder, "domain_indices"
        )

    def run(self, **kwargs: Any) -> None:
        """
        Regenerate domain index entries for a document.

        This happens near the end of processing a given document. This class
        need to be extended by providing a domain name and index class to
        be able to recreate the index instance and regenerate the entries.

        See also:
            It is extended in the compendia creation process. See
            :func:`sphinx_compendia.make_compendium`.

        Notes:
            This is a workaround for a limitation in Sphinx API: the domain
            indices are generated *before* cross-references are resolved.
            See :ref:`known-issues` for details.

        Args:
            **kwargs: We don't use these arguments.
        """
        domain_indices = getattr(self.app.builder, "domain_indices", [])

        # Find the domain index we are rebuilding
        index_number = 0
        for (
            index_name,
            index_class,
            original_entries_for_char,
            collapse,
        ) in domain_indices:
            if index_class == self.index_class:
                break
            index_number += 1
        else:
            return

        index = index_class(self.env.domains[self.domain_name])

        # Generate again the index
        regenerated, _ = index.generate([self.env.docname])

        new_entries_for_char = self._replace_entries(
            original_entries_for_char, regenerated
        )

        # Change the dict into the sorted list of tuples expected
        resorted = sorted(new_entries_for_char.items(), key=index.sort_key)

        # Replace the regenerated index
        domain_indices[index_number] = (
            index_name,
            index_class,
            resorted,
            collapse,
        )

    def _replace_entries(
        self,
        original_entries_for_char: List[Tuple[str, List[IndexEntry]]],
        regenerated: List[Tuple[str, List[IndexEntry]]],
    ) -> Dict[str, List[IndexEntry]]:
        # Use a dict instead of list of tuples expected
        new_entries_for_char = defaultdict(list, regenerated)
        current_docname = self.env.docname
        # Merge with entries not in this docname
        for character, entries in original_entries_for_char:
            new_entries = []
            for entry in entries:
                if current_docname != entry.docname:
                    new_entries.append(entry)
            new_entries_for_char[character].extend(new_entries)
        return new_entries_for_char
