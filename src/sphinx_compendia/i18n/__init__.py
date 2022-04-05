"""
Placeholder for our i18n.
"""

from __future__ import annotations

from gettext import NullTranslations
from pathlib import Path
from typing import Tuple

import sphinx.locale

locale_dir = Path(__file__).parent.resolve()

__all__ = [
    "t_",
    "t__",
    "init_console",
]

t_ = sphinx.locale._
t__ = sphinx.locale.__


def init_console(catalogue: str) -> Tuple[NullTranslations, bool]:
    return sphinx.locale.init_console(str(locale_dir), catalogue)
