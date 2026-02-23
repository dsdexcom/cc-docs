#!/usr/bin/env python3
"""Post-fetch cleaning pipeline for Claude Code documentation.

Transforms raw markdown from code.claude.com into lean, agent-optimized
content by removing Mintlify CMS artifacts, responsive image markup,
React components, and truncating the changelog.
"""

from __future__ import annotations

import logging
import re
import textwrap
import uuid

from collections.abc import Callable
from typing import TypeAlias

logger = logging.getLogger(__name__)

Rule: TypeAlias = Callable[[str], str]

# ---------------------------------------------------------------------------
# Cleaning statistics
# ---------------------------------------------------------------------------

_cleaning_stats: dict[str, int] = {"total_bytes_removed": 0, "files_cleaned": 0}


def log_cleaning_summary() -> None:
    """Log aggregate cleaning statistics."""
    total = _cleaning_stats["total_bytes_removed"]
    files = _cleaning_stats["files_cleaned"]
    tokens_est = total // 4  # rough: ~4 bytes per token
    logger.info(
        f"Cleaning summary: removed {total:,} bytes "
        f"(~{tokens_est:,} tokens) across {files} files"
    )


# ---------------------------------------------------------------------------
# Code-block protection
# ---------------------------------------------------------------------------


def _remove_theme_null(content: str) -> str:
    """Remove Mintlify ``theme={null}`` artifact from code fence lines.

    Runs before code-block protection so it catches all fence styles
    (3+ backticks, with or without extra info-string keywords).
    """
    return re.sub(
        r"^(\s*`{3,}[^\n]*?)\s+theme=\{null\}",
        r"\1",
        content,
        flags=re.MULTILINE,
    )


def _protect_code_blocks(content: str) -> tuple[str, dict[str, str]]:
    """Replace fenced code blocks with placeholders."""
    placeholders: dict[str, str] = {}

    def _replace(match: re.Match[str]) -> str:
        key = f"__CODEBLOCK_{uuid.uuid4().hex}__"
        placeholders[key] = match.group(0)
        return key

    # Match 3+ backtick fences; backreference ensures opening/closing match
    protected = re.sub(
        r"^(\s*(`{3,}))[^\n]*\n.*?^\s*\2\s*$",
        _replace,
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    return protected, placeholders


def _restore_code_blocks(content: str, placeholders: dict[str, str]) -> str:
    """Restore code blocks from placeholders."""
    for key, value in placeholders.items():
        content = content.replace(key, value)
    return content


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _dedent_content(text: str) -> str:
    """Dedent and strip tag content."""
    return textwrap.dedent(text).strip()


def _format_admonition(*, admonition_type: str, body: str) -> str:
    """Format admonition body as a markdown blockquote.

    Args:
        admonition_type: Label for the admonition (Note, Warning, etc.).
        body: Raw inner content of the admonition tag.

    Returns:
        Markdown blockquote string.
    """
    lines = _dedent_content(body).split("\n")
    result = [f"> **{admonition_type}:** {lines[0]}"]
    for line in lines[1:]:
        result.append(f"> {line}" if line.strip() else ">")
    return "\n".join(result)


# ---------------------------------------------------------------------------
# Doc rules — Anthropic docs only
# Order: structural wrappers → noise removal → semantic tag conversions
# ---------------------------------------------------------------------------


def strip_frame_tags(content: str) -> str:
    """Remove <Frame> wrapper tags, keeping inner content."""
    content = re.sub(r"^\s*<Frame>\s*$\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\s*</Frame>\s*$\n?", "", content, flags=re.MULTILINE)
    return content


def strip_div_wrappers(content: str) -> str:
    """Remove ``<div style={{...}}>`` wrapper tags, keeping inner content."""
    content = re.sub(
        r"^\s*<div\s+style=\{\{[^}]*\}\}>\s*$\n?", "", content, flags=re.MULTILINE
    )
    content = re.sub(r"^\s*</div>\s*$\n?", "", content, flags=re.MULTILINE)
    return content


def remove_doc_index_header(content: str) -> str:
    """Remove the 3-line Documentation Index blockquote header."""
    return re.sub(
        r"^> ## Documentation Index\n"
        r"> Fetch the complete documentation index at:[^\n]*\n"
        r"> Use this file to discover all available pages before exploring"
        r" further\.\n\n?",
        "",
        content,
        flags=re.MULTILINE,
    )


def simplify_img_tags(content: str) -> str:
    """Convert ``<img>`` tags to ``[Image: alt]`` and remove dark-mode duplicates."""
    # Remove dark-mode-only images entirely
    content = re.sub(
        r'^\s*<img\s[^>]*className="hidden dark:block"[^>]*>\s*\n?',
        "",
        content,
        flags=re.MULTILINE,
    )

    # Convert remaining img tags to markdown alt text
    def _replace_img(match: re.Match[str]) -> str:
        alt_match = re.search(r'alt="([^"]*)"', match.group(0))
        alt = alt_match.group(1) if alt_match else "image"
        return f"[Image: {alt}]"

    content = re.sub(r"<img\s[^>]*>", _replace_img, content)
    return content


def remove_mcp_registry_component(content: str) -> str:
    """Remove React MCPServersTable component and replace usage with link."""
    content = re.sub(
        r"^export const MCPServersTable\b.*?^};\s*$\n?",
        "",
        content,
        flags=re.MULTILINE | re.DOTALL,
    )
    content = re.sub(
        r"^\s*<MCPServersTable\b[^/]*/>\s*$",
        (
            "> Browse the MCP server registry at"
            " https://api.anthropic.com/mcp-registry/docs"
        ),
        content,
        flags=re.MULTILINE,
    )
    return content


def convert_admonitions(content: str) -> str:
    """Convert ``<Note>``, ``<Warning>``, ``<Tip>``, ``<Info>`` to blockquotes."""
    for tag in ("Note", "Warning", "Tip", "Info"):
        content = re.sub(
            rf"<{tag}>\s*(.*?)\s*</{tag}>",
            lambda m, t=tag: _format_admonition(admonition_type=t, body=m.group(1)),
            content,
            flags=re.DOTALL,
        )
    return content


def convert_tabs(content: str) -> str:
    """Convert ``<Tabs>/<Tab>`` to markdown using iterative inside-out nesting."""
    while "<Tabs>" in content:
        # Find innermost Tabs block (contains no nested <Tabs>)
        match = re.search(
            r"<Tabs>\s*\n((?:(?!<Tabs>).)*?)\s*</Tabs>",
            content,
            flags=re.DOTALL,
        )
        if not match:
            break

        inner = match.group(1)
        tabs = re.findall(
            r'<Tab title="([^"]*)">\s*\n?(.*?)\s*</Tab>',
            inner,
            flags=re.DOTALL,
        )

        parts = []
        for title, body in tabs:
            parts.append(f"**{title}:**\n\n{_dedent_content(body)}")

        replacement = "\n\n".join(parts)
        content = content[: match.start()] + replacement + content[match.end() :]

    return content


def convert_steps(content: str) -> str:
    """Convert ``<Steps>/<Step>`` to a numbered markdown list."""
    while "<Steps>" in content:
        match = re.search(
            r"<Steps>\s*\n(.*?)\s*</Steps>",
            content,
            flags=re.DOTALL,
        )
        if not match:
            break

        inner = match.group(1)
        steps = re.findall(
            r'<Step title="([^"]*)">\s*\n?(.*?)\s*</Step>',
            inner,
            flags=re.DOTALL,
        )

        parts = []
        for i, (title, body) in enumerate(steps, 1):
            parts.append(f"{i}. **{title}**\n\n{_dedent_content(body)}")

        replacement = "\n\n".join(parts)
        content = content[: match.start()] + replacement + content[match.end() :]

    return content


def convert_accordions(content: str) -> str:
    """Convert ``<Accordion>/<AccordionGroup>`` to markdown headers."""
    content = re.sub(r"^\s*<AccordionGroup>\s*$\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\s*</AccordionGroup>\s*$\n?", "", content, flags=re.MULTILINE)

    content = re.sub(
        r'<Accordion title="([^"]*)"[^>]*>\s*\n(.*?)\s*</Accordion>',
        lambda m: f"### {m.group(1)}\n\n{_dedent_content(m.group(2))}",
        content,
        flags=re.DOTALL,
    )
    return content


def convert_cards(content: str) -> str:
    """Convert ``<Card>/<CardGroup>`` to markdown bullet lists."""
    content = re.sub(r"^\s*<CardGroup[^>]*>\s*$\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\s*</CardGroup>\s*$\n?", "", content, flags=re.MULTILINE)

    def _replace_card(match: re.Match[str]) -> str:
        opening_tag = match.group(1)
        body = match.group(2).strip()

        title_match = re.search(r'title="([^"]*)"', opening_tag)
        href_match = re.search(r'href="([^"]*)"', opening_tag)

        title = title_match.group(1) if title_match else "Card"

        if href_match:
            link = f"[{title}]({href_match.group(1)})"
            return f"- **{link}**: {body}" if body else f"- **{link}**"

        return f"- **{title}**: {body}" if body else f"- **{title}**"

    content = re.sub(
        r"(<Card\s[^>]*>)\s*\n?(.*?)\s*</Card>",
        _replace_card,
        content,
        flags=re.DOTALL,
    )
    return content


# ---------------------------------------------------------------------------
# Changelog rules
# ---------------------------------------------------------------------------


def truncate_changelog(content: str) -> str:
    """Keep first 10 version sections, append link to full changelog."""
    version_pattern = re.compile(r"^## \d+\.\d+\.\d+", re.MULTILINE)
    matches = list(version_pattern.finditer(content))

    if len(matches) <= 10:
        return content

    cutoff = matches[10].start()
    truncated = content[:cutoff].rstrip()

    footer = (
        "\n\n---\n\n> Older versions omitted. Full changelog:"
        " https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
    )
    return truncated + footer


# ---------------------------------------------------------------------------
# Rule groups (explicit execution order)
# ---------------------------------------------------------------------------

DOC_RULES: tuple[Rule, ...] = (
    strip_frame_tags,
    strip_div_wrappers,
    remove_doc_index_header,
    simplify_img_tags,
    remove_mcp_registry_component,
    convert_admonitions,
    convert_tabs,
    convert_steps,
    convert_accordions,
    convert_cards,
)

CHANGELOG_RULES: tuple[Rule, ...] = (truncate_changelog,)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def clean_markdown_content(*, content: str, filename: str) -> str:
    """Clean raw markdown content for agent consumption.

    Args:
        content: Raw markdown content from fetch.
        filename: Target filename (used to select rule group).

    Returns:
        Cleaned markdown content.
    """
    original_size = len(content.encode("utf-8"))

    # Remove theme={null} before protection (operates on fence syntax)
    content = _remove_theme_null(content)
    content, placeholders = _protect_code_blocks(content)

    if filename == "changelog.md":
        rules = CHANGELOG_RULES
    else:
        rules = DOC_RULES

    for rule in rules:
        content = rule(content)

    content = _restore_code_blocks(content, placeholders)

    # Collapse 3+ consecutive blank lines to 2
    content = re.sub(r"\n{3,}", "\n\n", content)

    cleaned_size = len(content.encode("utf-8"))
    bytes_removed = original_size - cleaned_size
    _cleaning_stats["total_bytes_removed"] += bytes_removed
    _cleaning_stats["files_cleaned"] += 1

    if bytes_removed > 0:
        pct = bytes_removed / original_size if original_size > 0 else 0
        logger.debug(f"Cleaned {filename}: removed {bytes_removed:,} bytes ({pct:.1%})")

    return content
