from __future__ import annotations

from collections import defaultdict
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from sphinx.domains import Index as _Index
from sphinx.domains import IndexEntry

from sphinx_compendia.sphinxapi import SphinxDomainObjectDescription
from sphinx_compendia.store import Ref

T = TypeVar("T", bound="Index")


class Index(_Index):
    """
    A custom index that creates an NPC matrix.
    """

    def generate(
        self, docnames: Optional[Iterable[str]] = None
    ) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:
        """
        Generate domain index entries.

        Note:
             Entries should be filtered by the docnames provided. To do.

        Args:
            docnames: Restrict source Restructured text documents to these.

        Returns:
            See :meth:`sphinx.domains.Index.generate` for details.
        """
        grouped = self._get_indexable(docnames)

        index_dict = self._make_index_dict(grouped)

        # convert the dict to the sorted list of tuples expected
        content = sorted(index_dict.items(), key=self.sort_key)

        return content, True

    def sort_key(
        self, character_entries: Tuple[str, List[IndexEntry]]
    ) -> Tuple[str, List[IndexEntry]]:
        # sub index items have their own display name
        # ignore it in the sorting
        character, entries = character_entries
        return (
            character,
            [entry for entry in entries if entry.subtype in (0, 1)],
        )

    def _make_index_dict(
        self,
        grouped: Dict[str, List[Union[SphinxDomainObjectDescription, Ref]]],
    ) -> Dict[str, List[IndexEntry]]:
        content_working_copy = defaultdict(list)

        for display_name, entries in grouped.items():
            for letter, index_entry in self._gen_index_entries(
                display_name, entries
            ):
                content_working_copy[letter].append(index_entry)

        return content_working_copy

    def _get_indexable(
        self, docnames: Optional[Iterable[str]] = None
    ) -> Dict[str, List[Union[SphinxDomainObjectDescription, Ref]]]:
        grouped: Dict[
            str, List[Union[SphinxDomainObjectDescription, Ref]]
        ] = defaultdict(list)

        compendium_objects = self.domain.get_compendium_objects(docnames)  # type: ignore
        for compendium_object, objects in compendium_objects.items():
            for object_description in objects:
                grouped[compendium_object.primary_display_name].append(
                    object_description
                )
                references = self.domain.get_refs(object_description)  # type: ignore
                grouped[compendium_object.primary_display_name].extend(
                    references
                )

        return grouped

    def _gen_index_entries(
        self,
        display_name: str,
        entries: List[Union[SphinxDomainObjectDescription, Ref]],
    ) -> Iterator[Tuple[str, IndexEntry]]:
        # Generate the expected output, shown below, from the above using the
        # first letter of the objec diplay name as a key to group things
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        #
        # This shows:
        #
        #     D
        #   - **Display Name** *(extra info)* **qualifier:** typ
        #       **Sub Entry** *(extra info)* **qualifier:** typ
        SUBTYPE_NORMAL = 0
        SUBTYPE_WITHSUBS = 1  # noqa: F841
        SUBTYPE_SUB = 2  # noqa: F841

        if not entries:
            return []

        first_letter = display_name[0].lower()
        first_entry = entries[0]

        if not isinstance(first_entry, SphinxDomainObjectDescription):
            raise Exception()

        if len(entries) == 1:
            yield first_letter, IndexEntry(
                first_entry.dispname,
                SUBTYPE_NORMAL,
                first_entry.docname,
                first_entry.anchor,
                f"found in '{first_entry.docname}'",
                "",  # qualifier
                first_entry.type,
            )
        else:
            yield first_letter, IndexEntry(
                first_entry.dispname,
                SUBTYPE_WITHSUBS,
                first_entry.docname,
                first_entry.anchor,
                f"found in '{first_entry.docname}'",
                "",  # qualifier
                first_entry.type,
            )

            for other_entry in entries[1:]:
                qualifier = (
                    "alias"
                    if isinstance(other_entry, SphinxDomainObjectDescription)
                    else "xref"
                )
                yield first_letter, IndexEntry(
                    other_entry.dispname,
                    SUBTYPE_SUB,
                    other_entry.docname,
                    other_entry.anchor,
                    f"found in '{other_entry.docname}'",
                    qualifier,  # qualifier
                    first_entry.type,
                )
