#!/usr/bin/env python3
"""
Post-render script: resolves Quarto's <!-- desc(...) --> listing placeholders.

When using `type: custom` listings, Quarto doesn't auto-resolve description
placeholders. This script:
  - Extracts the first paragraph of each post (preserving <a> links)
  - Appends a "[N words]" word-count that links to the post
  - Embeds a YouTube video if the post contains one
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

OUTPUT_DIR = Path("_site")

# Matches the HTML-encoded placeholder Quarto leaves inside a <p> when type:custom is used
PLACEHOLDER_RE = re.compile(
    r'<(?P<tag>p|blockquote)[^>]*>\s*&lt;!-- desc\([^)]+\)\[max=(\d+)\]:([^\s]+) --&gt;\s*</(?P=tag)>',
    re.DOTALL,
)

YOUTUBE_RE = re.compile(r'youtube\.com/embed/([A-Za-z0-9_-]+)')


def inner_html_text_and_links(p) -> str:
    """Return inner content of a <p>, keeping <a> tags but stripping everything else."""
    parts = []
    for child in p.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif child.name == "a":
            href = child.get("href", "")
            text = child.get_text()
            if href and text:
                parts.append(f'<a href="{href}">{text}</a>')
            else:
                parts.append(child.get_text())
        else:
            parts.append(child.get_text())
    return "".join(parts).strip()


def extract_post_info(post_html_path: Path, max_len: int, post_url: str) -> dict:
    """Extract description text, word count, and optional YouTube embed from a post."""
    if not post_html_path.exists():
        return {}

    soup = BeautifulSoup(post_html_path.read_text(encoding="utf-8"), "html.parser")
    main = soup.select_one("main.content")
    if not main:
        return {}

    # Remove title block metadata before extracting content
    for meta in main.select(".quarto-title-meta, #title-block-header"):
        meta.decompose()

    # Total word count
    word_count = len(main.get_text(separator=" ", strip=True).split())

    # Quote posts (in quotes/ dir): extract the blockquote text as the description
    if str(post_html_path).find("/quotes/") != -1:
        blockquote = main.find("blockquote")
        if blockquote:
            return {"first_para": blockquote.get_text(separator=" ", strip=True), "youtube_embed": ""}

    # First substantive paragraph (preserving links when it fits; plain text when truncating)
    first_para = ""
    for p in main.find_all("p"):
        plain = p.get_text(separator=" ", strip=True)
        if len(plain) < 30:
            continue
        if len(plain) > max_len:
            # Truncate plain text at a word boundary — avoids cutting through <a> tags
            truncated = plain[:max_len].rsplit(" ", 1)[0]
            first_para = f'{truncated}… <a href="{post_url}">[{word_count:,} words]</a>'
        else:
            # Short enough to fit — preserve inner <a> links
            content = inner_html_text_and_links(p)
            first_para = f'{content} <a href="{post_url}">[{word_count:,} words]</a>'
        break

    # YouTube embed (first iframe with a YouTube src)
    youtube_embed = ""
    iframe = main.find("iframe", src=YOUTUBE_RE)
    if iframe:
        src = iframe["src"]
        youtube_embed = (
            f'<div class="plc-youtube-embed">'
            f'<iframe src="{src}" frameborder="0" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
            f'gyroscope; picture-in-picture" allowfullscreen></iframe>'
            f"</div>"
        )

    return {"first_para": first_para, "youtube_embed": youtube_embed}


def build_replacement(max_len: int, rel_path: str) -> str:
    post_html = OUTPUT_DIR / rel_path
    # URL: strip index.html suffix for clean links
    post_url = rel_path.replace("index.html", "").rstrip("/") + "/"
    info = extract_post_info(post_html, max_len, post_url)
    if not info:
        return ""

    parts = []
    if info.get("first_para"):
        if rel_path.startswith("quotes/"):
            parts.append(
                f'<blockquote class="plc-quote-block">{info["first_para"]}</blockquote>'
            )
        else:
            parts.append(
                f'<p class="plc-description listing-description">{info["first_para"]}</p>'
            )
    if info.get("youtube_embed"):
        parts.append(info["youtube_embed"])
    return "\n      ".join(parts)


def resolve_placeholders(listing_path: Path) -> None:
    content = listing_path.read_text(encoding="utf-8")

    def replace(match: re.Match) -> str:
        max_len = int(match.group(2))
        rel_path = match.group(3)
        return build_replacement(max_len, rel_path)

    new_content = PLACEHOLDER_RE.sub(replace, content)
    if new_content != content:
        listing_path.write_text(new_content, encoding="utf-8")
        print(f"  resolved descriptions in {listing_path}")


if __name__ == "__main__":
    listing_pages = {OUTPUT_DIR / "index.html"}
    for f in sys.argv[1:]:
        p = Path(f)
        if p.suffix == ".html":
            listing_pages.add(p)

    for page in listing_pages:
        if page.exists():
            resolve_placeholders(page)
