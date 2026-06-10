# Getting Started

## Downloading the game

Go to the **[Releases page](https://github.com/w1nterl0ng/heat-public/releases)** and download the zip for your platform:

| Platform | File | Notes |
|----------|------|-------|
| macOS | `HeatGame-mac-v*.zip` | Universal binary (Apple Silicon + Intel) |
| Windows | `HeatGame-win-v*.zip` | 64-bit |
| WebGL | `HeatGame-webgl-v*.zip` | Host locally via any web server |

The `releases/latest.json` file always points to the latest stable download URLs if you want to automate checks.

---

## macOS

1. Download `HeatGame-mac-v{version}-b{build}.zip` from the releases page.
2. Unzip — you will get `HeatGame.app`.
3. Move `HeatGame.app` to your Applications folder (optional).
4. On first launch, macOS may show a security warning because the app is not notarized. To open it:
   - Right-click (or Control-click) `HeatGame.app` → **Open**
   - Click **Open** in the dialog

---

## Windows

1. Download `HeatGame-win-v{version}-b{build}.zip`.
2. Unzip the folder anywhere (e.g. `C:\Games\Heat`).
3. Run `HeatGame.exe`.

---

## WebGL (browser)

1. Download `HeatGame-webgl-v{version}-b{build}.zip`.
2. Unzip it.
3. Serve the folder with any local web server, for example:

```bash
cd HeatGame-webgl-v0.1-b30
npx serve .
```

Then open **http://localhost:3000** in your browser. WebGL builds cannot be opened directly as `file://` due to browser security restrictions.

---

## Importing custom tracks

Tracks are created in the **[Heat Track Editor](https://w1nterl0ng.github.io/heat-track-editor/)** and exported as `track_{id}_v2_package.zip` files.

### Automatic import (beta testers)

1. Open Finder / Explorer and navigate to the game's persistent data folder:
   - **macOS:** `~/Library/Application Support/SlipStream/H-Game/TracksImport/`
   - **Windows:** `%APPDATA%\LocalLow\SlipStream\H-Game\TracksImport\`
2. Drop one or more `track_*_v2_package.zip` files into that folder.
3. Launch the game — it will import the tracks automatically on startup.

### Checking what's installed

Imported tracks appear on the track selection screen. If a track does not show up, check the in-game console log for `[TrackManager]` messages.
