import os
import re
import argparse
from datetime import datetime
from pathlib import Path

# --- Configuration ---
# Resolves the path relative to where this script is located (C:\PKM\Scripts)
VAULT_ROOT = Path(__file__).parent.parent
INBOX_DIR = VAULT_ROOT / "1_Inbox"

def ensure_directories():
    """Ensure the target directories exist."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

def generate_frontmatter(title, tags=None, source="CLI Pipeline"):
    """Generates standard Obsidian YAML frontmatter."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags_list = tags if tags else ["inbox", "unprocessed"]
    
    # Format tags for YAML list
    formatted_tags = "\n".join([f"  - {tag}" for tag in tags_list])
    
    frontmatter = f"""---
title: {title}
date: {date_str}
source: {source}
status: inbox
tags:
{formatted_tags}
---
"""
    return frontmatter

def sanitize_filename(title):
    """Removes illegal characters for Windows file paths."""
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def ingest_data(title, content, tags=None, source="CLI Pipeline"):
    """Creates the markdown file in the Obsidian inbox."""
    ensure_directories()
    
    safe_title = sanitize_filename(title)
    filename = f"{datetime.now().strftime('%Y%m%d%H%M')} - {safe_title}.md"
    file_path = INBOX_DIR / filename
    
    yaml_header = generate_frontmatter(title, tags, source)
    
    full_markdown = f"{yaml_header}\n# {title}\n\n{content}\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
        
    print(f"[SUCCESS] Ingested note: {file_path}")
    return file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest raw text into the Obsidian PKM Vault.")
    parser.add_argument("--title", required=True, help="The title of the note.")
    parser.add_argument("--content", required=True, help="The body content of the note.")
    parser.add_argument("--tags", nargs="+", help="Optional tags (without #).")
    parser.add_argument("--source", default="Manual Pipeline", help="Source of the data.")
    
    args = parser.parse_args()
    
    ingest_data(
        title=args.title,
        content=args.content,
        tags=args.tags,
        source=args.source
    )
