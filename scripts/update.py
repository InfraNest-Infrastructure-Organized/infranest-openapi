#!/usr/bin/env python3
"""Fetch InfraNest's published API description and write it here when it changed.

Writes openapi.json (pretty-printed, keys as published) and, when the description changed, a summary of what
changed to $GITHUB_OUTPUT / stdout: operations added, removed and changed. Exit 0 always unless the fetched
file is not a valid OpenAPI 3 description; an unreachable URL is a warning, not a failure.
"""
import hashlib
import json
import os
import pathlib
import sys
import urllib.request

URL = os.environ.get("OPENAPI_URL", "https://developers.infranest.io/openapi.json")
TARGET = pathlib.Path("openapi.json")


def operations(spec):
    out = {}
    for path, item in (spec.get("paths") or {}).items():
        for method, op in item.items():
            if method in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                out[f"{method.upper()} {path}"] = hashlib.sha256(json.dumps(op, sort_keys=True).encode()).hexdigest()
    return out


def summary(old, new):
    before, after = operations(old), operations(new)
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    lines = [f"{len(after)} operations: {len(added)} added, {len(removed)} removed, {len(changed)} changed."]
    for title, items in (("Added", added), ("Removed", removed), ("Changed", changed)):
        if items:
            lines += ["", f"### {title}", *[f"- `{item}`" for item in items]]
    return "\n".join(lines)


def main():
    try:
        with urllib.request.urlopen(URL, timeout=30) as answer:
            new = json.load(answer)
    except Exception as error:  # noqa: BLE001
        print(f"::warning::Could not fetch {URL} ({error}); nothing updated.")
        return
    if not str(new.get("openapi", "")).startswith("3.") or not new.get("paths"):
        sys.exit(f"{URL} is not an OpenAPI 3 description; refusing to publish it.")

    old = json.loads(TARGET.read_text()) if TARGET.exists() else {}
    text = json.dumps(new, indent=2, ensure_ascii=False) + "\n"
    if TARGET.exists() and TARGET.read_text() == text:
        print("No change.")
        return

    TARGET.write_text(text)
    notes = summary(old, new)
    print(notes)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as out:
            out.write("changed=true\n")
            out.write(f"notes<<NOTES_END\n{notes}\nNOTES_END\n")


if __name__ == "__main__":
    main()
