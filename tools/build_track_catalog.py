#!/usr/bin/env python3
"""Create the public catalog from manually reviewed track ZIP packages.

Usage:
  python3 tools/build_track_catalog.py /path/to/reviewed-zips \
    --release-base https://github.com/OWNER/REPO/releases/download/community-tracks

Only IDs listed in data/approved-tracks.json are published. That approval is
the deliberate human rights/content review gate; ZIP metadata cannot prove
that artwork is original or permission-cleared.
"""
import argparse, hashlib, json, shutil, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "data" / "approved-tracks.json"
OUTPUT = ROOT / "data" / "tracks.json"
PREVIEWS = ROOT / "assets" / "tracks"

def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)

def read_json(zf, filename):
    try:
        return json.loads(zf.read(filename))
    except KeyError: fail(f"{zf.filename}: missing {filename}")
    except json.JSONDecodeError as exc: fail(f"{zf.filename}: invalid {filename}: {exc}")

def public_record(zip_path, approved, base):
    with zipfile.ZipFile(zip_path) as zf:
        manifest = read_json(zf, "manifest.json")
        track_id = manifest.get("trackId")
        if not track_id or track_id not in approved:
            fail(f"{zip_path.name}: {track_id!r} is not in approved-tracks.json")
        v2_name = f"track_{track_id}_v2.json"
        track = read_json(zf, v2_name)
        preview_name = f"preview_{track_id}.jpg"
        try:
            preview = zf.read(preview_name)
        except KeyError: fail(f"{zip_path.name}: missing {preview_name}")
        if not preview.startswith(b"\xff\xd8\xff"):
            fail(f"{zip_path.name}: preview is not a JPEG")
        PREVIEWS.mkdir(parents=True, exist_ok=True)
        (PREVIEWS / preview_name).write_bytes(preview)

    required = ["name", "country", "version", "spaces", "corners", "defaultLaps"]
    missing = [key for key in required if not manifest.get(key) and manifest.get(key) != 0]
    if missing: fail(f"{zip_path.name}: manifest missing {', '.join(missing)}")
    if not track.get("designer") and not track.get("trackEditor"):
        fail(f"{zip_path.name}: V2 JSON missing designer/trackEditor credit")
    checksum = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    size = zip_path.stat().st_size
    return {
        "id": track_id, "name": manifest["name"], "country": manifest["country"],
        "designer": track.get("designer") or track["trackEditor"],
        "trackEditor": track.get("trackEditor"), "version": manifest["version"],
        "spaces": manifest["spaces"], "corners": manifest["corners"],
        "laps": manifest["defaultLaps"], "startingHeat": manifest.get("startingHeat"),
        "startingStress": manifest.get("startingStress"), "expansions": manifest.get("expansions", []),
        "tags": approved[track_id].get("tags", []),
        "preview": f"assets/tracks/{preview_name}",
        "download": f"{base.rstrip('/')}/{zip_path.name}",
        "size": f"{size / 1024 / 1024:.1f} MB", "checksum": f"sha256:{checksum}"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", type=Path)
    parser.add_argument("--release-base", required=True)
    args = parser.parse_args()
    if not args.packages.is_dir(): fail(f"not a folder: {args.packages}")
    approved = json.loads(APPROVED.read_text()).get("tracks", {})
    records = [public_record(path, approved, args.release_base)
               for path in sorted(args.packages.glob("track_*_v2_package.zip"))]
    if not records: fail("no track_*_v2_package.zip files found")
    records.sort(key=lambda item: (item["name"].casefold(), item["id"]))
    OUTPUT.write_text(json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(), "tracks": records}, indent=2) + "\n")
    print(f"Wrote {len(records)} tracks to {OUTPUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
