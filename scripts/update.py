#!/usr/bin/env python3
"""Fetch InfraNest's published API description and its collections, and write them here when they changed.

From the developer site (DEVELOPERS_URL, https://developers.infranest.io unless set):

- openapi.json                         the description (pretty-printed, keys as published)
- postman/infranest.postman_collection.json and postman/infranest.postman_environment.json
- bruno/                               the Bruno collection, unpacked from infranest.bruno.zip, so it can be
                                       opened from a clone and its changes read in a diff
- .spectral.yaml                       the lint ruleset (spectral.yaml on the site), which CI runs on openapi.json

When anything changed, writes `changed=true` and release notes to $GITHUB_OUTPUT: the operations added, removed and
changed, and which collections changed. Exits 0 unless a fetched description is not valid OpenAPI 3 or a collection
is malformed; an unreachable site is a warning, not a failure, and changes nothing.
"""
import hashlib
import io
import json
import os
import pathlib
import shutil
import sys
import urllib.request
import zipfile

SITE = os.environ.get("DEVELOPERS_URL", "https://developers.infranest.io").rstrip("/")
# Kept for the old setting: OPENAPI_URL still points the description elsewhere.
OPENAPI_URL = os.environ.get("OPENAPI_URL", f"{SITE}/openapi.json")
ROOT = pathlib.Path(".")


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as answer:
        return answer.read()


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


def pretty(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write(path, text):
    """Write `text` to `path`; True when that changed the file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == text.encode():
        return False
    path.write_text(text)
    return True


def bruno_files(archive):
    """The collection's files from the zip, under its single `infranest/` folder, as {relative path: bytes}."""
    files = {}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        for name in z.namelist():
            if name.endswith("/"):
                continue
            parts = pathlib.PurePosixPath(name).parts
            if parts[0] != "infranest" or ".." in parts or len(parts) < 2:
                sys.exit(f"Unexpected file in the Bruno collection: {name}")
            files[str(pathlib.PurePosixPath(*parts[1:]))] = z.read(name)
    if "bruno.json" not in files:
        sys.exit("The Bruno collection has no bruno.json; refusing to publish it.")
    return files


def sync_bruno(files):
    """Replace bruno/ with exactly these files; True when anything differs."""
    target = ROOT / "bruno"
    current = {}
    if target.exists():
        current = {str(p.relative_to(target).as_posix()): p.read_bytes() for p in target.rglob("*") if p.is_file()}
    if current == files:
        return False
    if target.exists():
        shutil.rmtree(target)
    for rel, data in files.items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return True


def main():
    try:
        new = json.loads(fetch(OPENAPI_URL))
        postman = json.loads(fetch(f"{SITE}/infranest.postman_collection.json"))
        environment = json.loads(fetch(f"{SITE}/infranest.postman_environment.json"))
        bruno = fetch(f"{SITE}/infranest.bruno.zip")
        ruleset = fetch(f"{SITE}/spectral.yaml").decode()
    except Exception as error:  # noqa: BLE001
        print(f"::warning::Could not fetch from {SITE} ({error}); nothing updated.")
        return

    if not str(new.get("openapi", "")).startswith("3.") or not new.get("paths"):
        sys.exit(f"{OPENAPI_URL} is not an OpenAPI 3 description; refusing to publish it.")
    if "info" not in postman or "item" not in postman:
        sys.exit("The Postman collection is not a collection; refusing to publish it.")
    if any(v.get("key") == "token" and v.get("value") for v in environment.get("values", [])):
        sys.exit("The Postman environment carries a token value; refusing to publish it.")

    target = ROOT / "openapi.json"
    old = json.loads(target.read_text()) if target.exists() else {}
    notes = []
    if write(target, pretty(new)):
        notes.append(summary(old, new))
    collections = []
    if write(ROOT / "postman" / "infranest.postman_collection.json", pretty(postman)):
        collections.append("the Postman collection")
    if write(ROOT / "postman" / "infranest.postman_environment.json", pretty(environment)):
        collections.append("the Postman environment")
    if sync_bruno(bruno_files(bruno)):
        collections.append("the Bruno collection")
    ruleset_changed = write(ROOT / ".spectral.yaml", ruleset)
    if collections:
        notes.append("Updated: " + ", ".join(collections) + ".")
    if ruleset_changed:
        notes.append("The lint ruleset (`.spectral.yaml`) changed.")

    if not notes:
        print("No change.")
        return

    text = "\n\n".join(notes)
    print(text)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as out:
            out.write("changed=true\n")
            out.write(f"notes<<NOTES_END\n{text}\nNOTES_END\n")


if __name__ == "__main__":
    main()
