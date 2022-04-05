from __future__ import annotations

import re

import pytest


@pytest.mark.sphinx(testroot="basic")
def test_basic(built_index_html: str, status, warning):
    html = (
        r"<h1>test-basic<a "
        r'class="headerlink" '
        r'href="#test-basic" '
        r'title="Permalink to this headline">¶'
        r"</a></h1>"
    )

    assert re.search(html, built_index_html, re.DOTALL)


@pytest.mark.sphinx(testroot="full")
def test_full(built_index_html: str, status, warning):
    print(built_index_html)
    assert True


@pytest.fixture()
def built_index_html(app, outdir) -> str:
    out_file = app.outdir / "index.html"

    content = out_file.read_text()
    return content


@pytest.fixture()
def outdir(app):
    app.builder.build_all()
    return app.outdir
