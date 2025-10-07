#!/usr/bin/env python3
"""
Create milestones (one per story) and issues (one per Task section) from markdown files
inside docs/stories/*.md in your repo.

Usage:
  export GITHUB_TOKEN=ghp_xxx
  export REPO=owner/repo   # e.g., hariseldon84/decodebyanand
  python tools/create_issues_from_stories.py --root . --dry-run
  python tools/create_issues_from_stories.py --root .

Notes
- Detects tasks only in the "## Tasks" / "## Tasks / Subtasks" section.
- Accepts bullets/checkboxes and bold:  - [ ] **Task 3: Title** (AC: ...)
- Skips duplicates by preloading titles for the milestone (no Search API).
- Auto waits if GitHub core rate limit is hit.
"""

import os
import re
import sys
import time
import argparse
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import requests

GITHUB_API = "https://api.github.com"

# ----------------------- small utils -----------------------

def log(msg: str) -> None:
    print(msg, flush=True)

def load_md(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()

def humanize_filename(name: str) -> str:
    cleaned = re.sub(r"^\d+(\.\d+)*-?", "", name)
    cleaned = re.sub(r"[-_]+", " ", cleaned).strip()
    return cleaned[:1].upper() + cleaned[1:]

H1_RE = re.compile(r"^#\s+(.+)$")

def find_story_title(lines: List[str], fallback_filename: str) -> str:
    for ln in lines[:30]:
        m = H1_RE.match(ln.strip())
        if m:
            title = m.group(1).strip()
            if not re.search(r"tasks?\s*/\s*subtasks?", title, re.I):
                return title
    return humanize_filename(fallback_filename)

# -------------------- task parsing (tailored to your format) --------------------

TASKS_HDR_RE = re.compile(r"^\s*#{2,6}\s*Tasks(?:\s*/\s*Subtasks)?\s*$", re.IGNORECASE)

TASK_ANCHOR_RE = re.compile(
    r"""^\s*
        [\-–—•]\s*                # bullet
        \[\s*[xX ]?\s*\]\s*       # checkbox
        (?:\*\*)?\s*              # optional opening bold
        Task\s*(\d+)\s*:\s*(.+?)  # Task N: Title
        (?:\*\*)?\s*              # optional closing bold
        (?:\s*\(AC:[^)]+\))?      # optional (AC: ...)
        \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

def slice_tasks_section(lines: List[str]) -> List[str]:
    start = None
    for i, ln in enumerate(lines):
        if TASKS_HDR_RE.match(ln.strip()):
            start = i + 1
            break
    if start is None:
        return []
    # end at next header (## or #)
    end = len(lines)
    for j in range(start, len(lines)):
        s = lines[j].lstrip()
        if s.startswith("##") or s.startswith("# "):
            end = j
            break
    return lines[start:end]

def chunk_tasks(lines: List[str]) -> List[Tuple[str, str]]:
    section = slice_tasks_section(lines)
    if not section:
        return []
    anchors: List[Tuple[int, str]] = []
    for i, raw in enumerate(section):
        m = TASK_ANCHOR_RE.match(raw)
        if m:
            num = m.group(1)
            title = m.group(2).strip()
            title = re.sub(r"\s*\(AC:[^)]+\)\s*$", "", title).strip()
            anchors.append((i, f"Task {num}: {title}"))
    if not anchors:
        return []
    anchors.append((len(section), None))  # sentinel
    tasks: List[Tuple[str, str]] = []
    for (start_idx, issue_title), (next_idx, _) in zip(anchors[:-1], anchors[1:]):
        body = "\n".join(section[start_idx + 1 : next_idx]).strip()
        tasks.append((issue_title, body))
    return tasks

# ----------------------- GitHub API helpers -----------------------

def gh_request(method: str, url: str, token: str, **kwargs):
    """Core REST request with simple rate-limit backoff."""
    headers = kwargs.pop("headers", {})
    headers.update({
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "stories-to-issues-script"
    })
    while True:
        resp = requests.request(method, url, headers=headers, **kwargs)
        if resp.status_code == 403:
            # rate limit backoff
            try:
                remaining = int(resp.headers.get("X-RateLimit-Remaining", "1"))
                reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
            except ValueError:
                remaining, reset = 1, 0
            if remaining == 0:
                wait_s = max(reset - int(time.time()) + 2, 5)
                log(f"Hit GitHub rate limit. Sleeping {wait_s}s then retrying...")
                time.sleep(wait_s)
                continue
        if resp.status_code >= 400:
            raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text}")
        return resp

def get_existing_milestones(repo: str, token: str) -> Dict[str, Dict]:
    # paginate (just in case)
    page = 1
    out: Dict[str, Dict] = {}
    while True:
        url = f"{GITHUB_API}/repos/{repo}/milestones?state=all&per_page=100&page={page}"
        data = gh_request("GET", url, token).json()
        if not data:
            break
        for m in data:
            out[m["title"].strip()] = m
        page += 1
    return out

def ensure_milestone(repo: str, token: str, title: str, dry_run: bool=False) -> Dict:
    existing = get_existing_milestones(repo, token)
    if title in existing:
        log(f"Milestone exists: {title}")
        return existing[title]
    payload = {"title": title}
    log(f"Creating milestone: {title}")
    if dry_run:
        return {"number": None, "title": title}
    return gh_request("POST", f"{GITHUB_API}/repos/{repo}/milestones", token, json=payload).json()

def get_issue_titles_for_milestone(repo: str, token: str, milestone_number: Optional[int]) -> set:
    """Return lowercase titles of all issues in a milestone (state=all)."""
    titles = set()
    if not milestone_number:
        return titles
    page = 1
    while True:
        url = (f"{GITHUB_API}/repos/{repo}/issues"
               f"?state=all&milestone={milestone_number}&per_page=100&page={page}")
        data = gh_request("GET", url, token).json()
        if not data:
            break
        for it in data:
            if "pull_request" in it:
                continue
            titles.add(it["title"].strip().lower())
        page += 1
    return titles

def create_issue(repo: str, token: str, title: str, body: str, milestone_number: Optional[int], labels: List[str], dry_run: bool=False) -> Dict:
    payload = {"title": title, "body": body}
    if milestone_number:
        payload["milestone"] = milestone_number
    if labels:
        payload["labels"] = labels
    log(f"Creating issue: {title}")
    if dry_run:
        return {"number": None, "title": title}
    return gh_request("POST", f"{GITHUB_API}/repos/{repo}/issues", token, json=payload).json()

# ----------------------------- main -----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo working directory (contains docs/stories)")
    ap.add_argument("--docs-subdir", default="docs/stories", help="Path to stories under root")
    ap.add_argument("--labels", default="story,task", help="Comma list of labels for created issues")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    repo = os.getenv("REPO")
    if not token:
        print("ERROR: GITHUB_TOKEN/GH_TOKEN env var is required", file=sys.stderr)
        sys.exit(2)
    if not repo:
        print("ERROR: REPO env var (owner/repo) is required", file=sys.stderr)
        sys.exit(2)

    root = Path(args.root).resolve()
    stories_dir = (root / args.docs_subdir).resolve()
    if not stories_dir.exists():
        print(f"ERROR: stories directory not found: {stories_dir}", file=sys.stderr)
        sys.exit(2)

    labels = [x.strip() for x in args.labels.split(",") if x.strip()]
    md_files = sorted(stories_dir.glob("*.md"))
    if not md_files:
        log("No story markdown files found.")
        sys.exit(0)

    for md in md_files:
        lines = load_md(md)
        story_title = find_story_title(lines, md.stem)
        milestone = ensure_milestone(repo, token, story_title, dry_run=args.dry_run)
        milestone_number = milestone.get("number")

        # Parse tasks from the story’s Tasks section
        tasks = chunk_tasks(lines)

        # Dry-run visibility
        if args.dry_run:
            if tasks:
                log(f"[DRY-RUN] {md.name}: {len(tasks)} task(s)")
                for t, _ in tasks:
                    log(f"  -> {t}")
            else:
                log(f"[DRY-RUN] {md.name}: no task anchors found; would create placeholder issue")

        # If no tasks detected, create a single placeholder
        if not tasks:
            tasks = [(f"{story_title}: Review & Break Down", "\n".join(lines))]

        # Preload existing issue titles for this milestone (state=all)
        existing_titles = set()
        if milestone_number:
            existing_titles = get_issue_titles_for_milestone(repo, token, milestone_number)

        # Create issues
        for issue_title, body in tasks:
            if issue_title.strip().lower() in existing_titles:
                log(f"Issue exists: {issue_title}")
                continue
            body_final = f"{body}\n\n—\nSource: `{md.as_posix()}`"
            try:
                create_issue(repo, token, issue_title, body_final, milestone_number, labels, dry_run=args.dry_run)
                existing_titles.add(issue_title.strip().lower())
            except RuntimeError as e:
                log(f"Failed to create issue '{issue_title}': {e}")
                continue

    log("Done.")

if __name__ == "__main__":
    main()
