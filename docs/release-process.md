# Release Process

## Version numbering

Builds use a two-part identifier:

| Component | Source | Example |
|-----------|--------|---------|
| Semantic version | Unity `bundleVersion` in Project Settings | `0.1` |
| Build number | `Assets/Resources/BuildInfo.txt` (auto-incremented) | `30` |
| Combined tag | `v{version}-b{build}` | `v0.1-b30` |
| In-game display | `v0.1  build 30` | shown in the bottom-right corner |

The semantic version changes with significant milestone releases. The build number increments with every `Build All` run.

---

## Release channels

| Channel | Tag format | Notes |
|---------|------------|-------|
| Stable | `v0.1-b30` | Full release — manually triggered |
| Nightly | `nightly-2026-06-10-b31` | Automated daily build — pre-release, kept for 7 days |

Nightly builds are marked as pre-releases on GitHub. The stable `releases/latest.json` manifest is only updated on stable releases.

---

## Stable release workflow

1. In the Unity editor, run **Heat → Build All and Publish**.
2. Confirm the version and build number in the dialog.
3. The editor runs the build, packages the zips, and creates a GitHub Release on `w1nterl0ng/heat-public`.
4. The release includes:
   - `HeatGame-mac-v0.1-b30.zip` + `.sha256`
   - `HeatGame-win-v0.1-b30.zip` + `.sha256`
   - `HeatGame-webgl-v0.1-b30.zip` + `.sha256`
5. `releases/latest.json` is updated in this repo to point to the new release.

### From the command line

```bash
cd tools/release
./package.sh                             # zip the latest Builds/ output
./publish.sh --channel stable            # create GitHub Release on heat-public
```

Use `--dry-run` to preview without uploading:

```bash
./publish.sh --channel stable --dry-run
```

---

## Nightly build workflow

Nightly builds run automatically at 06:00 UTC via GitHub Actions (self-hosted Mac runner in the private `heat-unity` repo). They build all platforms, package, and publish as a pre-release tagged `nightly-{date}-b{build}`.

You can also trigger a nightly manually from the **Actions** tab in the `w1nterl0ng/heat-unity` repo.

Old nightly releases (> 7 days) are pruned automatically by the publish script.

---

## Artifact checksums

Every zip has a companion `.sha256` file containing the SHA-256 hash of the zip. To verify a download on macOS/Linux:

```bash
shasum -a 256 HeatGame-mac-v0.1-b30.zip
# compare the output against HeatGame-mac-v0.1-b30.sha256
```

---

## Credentials required

The publish script uses the `gh` CLI. For local use, `gh auth login` once is enough. For CI, a fine-grained GitHub PAT with `contents:write` on `heat-public` is stored as the `HEAT_PUBLIC_RELEASE_TOKEN` secret in the `heat-unity` repo.
