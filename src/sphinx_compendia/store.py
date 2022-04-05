from __future__ import annotations

from collections import defaultdict
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Set,
    Tuple,
    Type,
    TypeVar,
)

from sphinx import addnodes
from sphinx.util.logging import getLogger

from sphinx_compendia.i18n import t__
from sphinx_compendia.sphinxapi import SphinxDomainObjectDescription

log = getLogger(__name__)


class CompendiumObject(NamedTuple):
    """
    Store documented domain objects in a Sphinx domain data.
    """

    object_id: str
    """
    Identify this object.
    """

    objtype: str
    """
    Constituent typename this object represents.
    """

    objtype_alias: str
    """
    The directive name this constituent was documented with.
    """

    primary_display_name: str
    """
    Human readable name for this object, the first signature from its directive.
    """


TD = TypeVar("TD", bound="CompendiumData")


class Ref(NamedTuple):
    dispname: str
    docname: str
    anchor: str


class CompendiumData(NamedTuple):
    object_descriptions: Dict[str, List[SphinxDomainObjectDescription]]
    compendium_objects: Dict[str, CompendiumObject]
    objtype_selectors: Dict[str, Dict[str, Set[str]]]
    signature_references: Dict[SphinxDomainObjectDescription, List[Ref]]
    admissible_parent_objtypes: Dict[str, Set[str]]
    children: Dict[str, Set[str]]
    namespaces: Dict[str, str]

    @classmethod
    def initial_data(
        cls: Type[TD],
        objtypes: Iterable[str],
        admissible_parent_objtypes: Dict[str, Set[str]],
    ) -> TD:
        return cls(
            defaultdict(list),
            {},
            {objtype: defaultdict(set) for objtype in objtypes},
            defaultdict(list),
            admissible_parent_objtypes,
            defaultdict(set),
            {},
        )

    def add_object(
        self,
        objtype: str,
        objtype_alias: str,
        object_id: str,
        object_description: SphinxDomainObjectDescription,
        namespace: List[str],
        signode: addnodes.desc_signature,
    ) -> None:
        if object_id not in self.compendium_objects:
            new_namespace = ".".join([*namespace, object_description.dispname])
            if new_namespace in self.namespaces:
                log.warning(
                    t__("object with namespace %s already documented"),
                    new_namespace,
                    location=signode,
                )
            self.compendium_objects[object_id] = CompendiumObject(
                object_id, objtype, objtype_alias, object_description.dispname
            )
            self.namespaces[new_namespace] = object_id

        if len(namespace) > 1:
            for parent_compendium_object, _ in self.find(
                self.admissible_parent_objtypes[objtype],
                ".".join(namespace[0:-1]),
            ):
                self.children[parent_compendium_object.object_id].add(object_id)

        self.object_descriptions[object_id].append(object_description)
        self.objtype_selectors[objtype][object_description.dispname].add(
            object_id
        )

    def add_backref(
        self,
        object_description: SphinxDomainObjectDescription,
        docname: str,
        anchor: str,
        display_name: str,
    ) -> None:
        self.signature_references[object_description].append(
            Ref(display_name, docname, anchor)
        )

    def find_object_descriptions(
        self,
    ) -> Iterable[SphinxDomainObjectDescription]:
        for object_descriptions in self.object_descriptions.values():
            yield from object_descriptions

    def find(
        self, objtypes: Iterable[str], target: str
    ) -> Iterator[Tuple[CompendiumObject, SphinxDomainObjectDescription]]:
        *parent_selectors, terminal_selector = target.split(".")

        for compendium_object in self._find_compendium_objects(
            objtypes, target
        ):
            for object_description in self.object_descriptions[
                compendium_object.object_id
            ]:
                if terminal_selector == object_description.dispname:
                    yield compendium_object, object_description

    def _find_compendium_objects(
        self, objtypes: Iterable[str], target: str
    ) -> Iterable[CompendiumObject]:
        *parent_selectors, terminal_selector = target.split(".")

        filter = self._make_filter(parent_selectors)

        for objtype in objtypes:
            for object_id in self.objtype_selectors[objtype][terminal_selector]:
                compendium_object = self.compendium_objects[object_id]
                if not filter(compendium_object):
                    continue
                yield compendium_object

    def _make_filter(
        self, parent_selectors: List[str]
    ) -> Callable[[CompendiumObject], bool]:
        if parent_selectors:

            filter = self._make_parent_filter(parent_selectors)

        else:

            def filter(compendium_object: CompendiumObject) -> bool:
                return True

        return filter

    def _make_parent_filter(
        self, parent_selectors: List[str]
    ) -> Callable[[CompendiumObject], bool]:
        def filter(compendium_object: CompendiumObject) -> bool:
            parent_objtypes = self.objtype_selectors.keys()
            for parent_compendium_object, _ in self.find(
                parent_objtypes, ".".join(parent_selectors)
            ):
                if (
                    compendium_object.object_id
                    in self.children[parent_compendium_object.object_id]
                ):
                    return True
            else:
                return False

        return filter
