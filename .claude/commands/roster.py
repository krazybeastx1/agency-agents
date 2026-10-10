#!/usr/bin/env python3
"""Emit the installed Claude Code subagent roster grouped by division.

Reads ~/.claude/agents/*.md and groups each agent by its agency-agents
division. Division membership comes from the source repo (divisions.json +
per-division agent `name:`), because installed filenames are not reliably
division-prefixed. Falls back to filename-prefix grouping when the source
repo cannot be found.

Output: one line per division as `stem=>Name` pairs. The frontmatter `name:`
is what Claude Code's Task tool expects for `subagent_type`.
"""
import os
import re

HOME = os.path.expanduser("~")
AGENTS = os.path.join(HOME, ".claude", "agents")

# Fallback division keys + labels (mirrors divisions.json in agency-agents).
FALLBACK = [
    ("game-development", "Game Development"),
    ("project-management", "Project Management"),
    ("spatial-computing", "Spatial Computing"),
    ("academic", "Academic"),
    ("design", "Design"),
    ("engineering", "Engineering"),
    ("finance", "Finance"),
    ("healthcare", "Healthcare"),
    ("marketing", "Marketing"),
    ("paid-media", "Paid Media"),
    ("product", "Product"),
    ("research", "Research"),
    ("sales", "Sales"),
    ("security", "Security"),
    ("specialized", "Specialized"),
    ("support", "Support"),
    ("testing", "Testing"),
    ("gis", "GIS"),
]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def field(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % key, fm, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    for ln in fm[m.end():].split("\n"):
        if re.match(r"^\s+\S", ln):
            v += " " + ln.strip()
        else:
            break
    v = v.strip()
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1].replace("''", "'")
    return v


def name_of(path):
    return field(frontmatter(open(path, encoding="utf-8").read()), "name")


def find_repo():
    candidates = []
    env = os.environ.get("AGENCY_AGENTS_DIR")
    if env:
        candidates.append(env)
    candidates.append(os.path.join(HOME, "agency-agents"))
    candidates.append(os.path.join(HOME, "dev", "agency-agents"))
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        candidates.append(d)
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    for c in candidates:
        if c and os.path.isfile(os.path.join(c, "divisions.json")):
            return c
    return None


def load_divisions(repo):
    """Return (ordered list of (key,label), name->division) from the source repo."""
    import json

    divs = json.load(open(os.path.join(repo, "divisions.json"), encoding="utf-8"))["divisions"]
    order = [(k, divs[k].get("label", k)) for k in divs]
    name_to_div = {}
    for key in divs:
        ddir = os.path.join(repo, key)
        if not os.path.isdir(ddir):
            continue
        for root, _dirs, files in os.walk(ddir):
            for f in files:
                if f.endswith(".md"):
                    nm = name_of(os.path.join(root, f))
                    if nm:
                        name_to_div[nm] = key
    return order, name_to_div


def division_by_prefix(stem, keys):
    best = None
    for key in keys:
        if stem == key or stem.startswith(key + "-"):
            if best is None or len(key) > len(best):
                best = key
    return best


def main():
    repo = find_repo()
    if repo:
        order, name_to_div = load_divisions(repo)
    else:
        order, name_to_div = FALLBACK, {}
    keys = [k for k, _ in order]
    labels = dict(order)

    groups = {k: [] for k in keys}
    other = []
    for f in sorted(os.listdir(AGENTS)):
        if not f.endswith(".md"):
            continue
        stem = f[:-3]
        nm = name_of(os.path.join(AGENTS, f)) or stem
        div = name_to_div.get(nm) or division_by_prefix(stem, keys)
        entry = "%s=>%s" % (stem, nm)
        if div in groups:
            groups[div].append(entry)
        else:
            other.append(entry)

    print("DIVISIONS: " + ",".join(keys))
    for key in keys:
        if groups[key]:
            print("%s (%s): %s" % (key, labels[key], ", ".join(groups[key])))
    if other:
        print("other (Other): %s" % ", ".join(other))


main()
