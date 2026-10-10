#!/usr/bin/env python3
"""Emit the installed agency-agents roster grouped by division.

Derives the division set from divisions.json (the single source of truth),
maps every installed subagent id (slugified `name:` in .opencode/agents/) to
its source division, and prints one line per division. cwd-independent: the
repo root is inferred from this file's location.
"""
import json
import os
import re

def repo_root(start):
    """Nearest ancestor of this file that holds divisions.json (cwd-independent)."""
    d = os.path.dirname(os.path.abspath(start))
    while True:
        if os.path.isfile(os.path.join(d, "divisions.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


ROOT = repo_root(__file__)
if not ROOT:
    raise SystemExit("roster.py: divisions.json not found above %s" % __file__)
Q = "\"'"


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


def slugify(s):
    s = re.sub(r"[^a-z0-9]", "-", s.lower())
    return re.sub(r"-+", "-", s).strip("-")


def looks_like_fmt(text):
    """Return the frontmatter body if the file starts with a YAML fence."""
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


divs = json.load(open(os.path.join(ROOT, "divisions.json")))["divisions"]
agentdir = os.path.join(ROOT, ".opencode", "agents")
installed = {f[:-3] for f in os.listdir(agentdir) if f.endswith(".md")}

lines = ["DIVISIONS: " + ",".join(divs)]
for div in divs:
    ddir = os.path.join(ROOT, div)
    if not os.path.isdir(ddir):
        continue
    members = []
    for root, _dirs, files in os.walk(ddir):
        for f in files:
            if not f.endswith(".md"):
                continue
            fm = looks_like_fmt(open(os.path.join(root, f), encoding="utf-8").read())
            if not fm:
                continue
            name = field(fm, "name")
            if name and slugify(name) in installed:
                members.append(slugify(name))
    label = divs[div].get("label", div)
    lines.append("%s (%s): %s" % (div, label, ",".join(sorted(members))))

print("\n".join(lines))