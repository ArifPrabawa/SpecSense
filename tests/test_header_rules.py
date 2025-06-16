from app.header_rules import (
    is_markdown_header,
    is_numbered_header,
    is_all_caps_header,
    is_isolated_all_caps_header,
)


def test_markdown_header():
    assert is_markdown_header("# Introduction")
    assert not is_markdown_header("Introduction")


def test_numbered_header():
    assert is_numbered_header("1. Overview")
    assert is_numbered_header("3.1.2 Scope")
    assert not is_numbered_header("Version 3.1")


def test_all_caps_header():
    assert is_all_caps_header("SYSTEM OVERVIEW")
    assert not is_all_caps_header("System Overview")


def test_isolated_all_caps():
    # All-caps line with blank line above
    assert is_isolated_all_caps_header("LOGIN", "", "Body")
    # All-caps line with blank line below
    assert is_isolated_all_caps_header("LOGIN", "Body", "")
    # Not isolated (text above and below)
    assert not is_isolated_all_caps_header("LOGIN", "Prev", "Next")
