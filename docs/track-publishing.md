# Publishing reviewed community tracks

1. Collect reviewed `track_*_v2_package.zip` packages in one local folder.
2. Add each reviewed ID and optional discovery tags to `data/approved-tracks.json`. This is the human approval gate; do not add packages with official scans, copied official artwork, uncertain credit, or unresolved rights concerns.
3. Generate the catalog:

   ```bash
   python3 tools/build_track_catalog.py /path/to/packages \
     --release-base https://github.com/w1nterl0ng/heat-public/releases/download/community-tracks
   ```

4. Review the generated `data/tracks.json` and previews in `assets/tracks/`.
5. Create or update the `community-tracks` GitHub Release and upload the same ZIPs as assets.
6. Commit `data/tracks.json`, `assets/tracks/`, and approval changes. Do not commit the ZIPs to the Pages repository.
7. Verify each library card downloads the matching release asset and imports in the game.

The generator rejects missing manifests, V2 JSON, previews, credit, required metadata, and any package ID absent from the approval list. It cannot determine ownership of artwork—review that manually.

## Supported-track updates

`data/tracks.json` is the catalog the site renders and the file a future game client should poll. The public URL is `https://w1nterl0ng.github.io/heat-public/data/tracks.json`.

Supported tracks are exactly the `id` values in that file. A package someone imported privately is not updated.

When the game adds a track check, it should:

- Fetch that URL and ignore JSON fields it does not recognize.
- Match each catalog `id` to an installed `trackId`.
- Treat catalog `version` as newer when it sorts after the installed version with an ordinal string compare. Publish versions as `YYYY-MM-DD` so that compare stays valid.
- Download the catalog `download` URL and import that ZIP with the existing package importer.
- Compare `version` strings. Do not compare the catalog `checksum` (a hash of the ZIP) with the game's track-JSON checksum. They are different hashes.

Keep download URLs on the `community-tracks` GitHub Release. Do not commit the ZIP packages to this repository.
