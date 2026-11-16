---
name: free-my-tv
description: Build, install, configure, and customize Free My TV (simbasjungles/free-my-tv) on Google TV, Android TV, LG webOS, and Samsung Tizen TVs. Use when the user asks to replace an ad-heavy TV home screen, sideload or build FreeMyTV.apk, configure config.properties, send Home Assistant or Immich keys, or revert to the stock launcher.
allowed-tools: client
---
# Free My TV

Set up, build, install, and customize [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv), an ad-free home screen for Google TV, Android TV, LG webOS, and Samsung Tizen with one-button undo (`Free My TV -> Home Screen -> Original`).

## When to Use

- The user wants to install or build Free My TV on a Google TV, Android TV, LG webOS, or Samsung Tizen TV.
- The user wants to customize `config.properties`, shelf apps (`SHELF`), debloat lists (`DEBLOAT`), translations (`tools/translate.py`), or integrations (TMDB, Watchmode, Plex, Trakt, Home Assistant, Immich).
- The user needs to send photos (`tools/photos.py`) or secrets (`tools/send_key.py`) to the TV, or revert to the stock home screen.

## Steps

### 1. Clone the Repository and Identify the TV Platform

Ask for the TV's IP address, platform (Google TV/Android TV, LG webOS, or Samsung Tizen), and city if not provided, then clone the repo:

```bash
git clone https://github.com/simbasjungles/free-my-tv.git && cd free-my-tv
```

### 2. Build and Install by Platform

- **Google TV / Android TV (Android 8+)**:
  1. Ensure JDK 17+, Android SDK (`build-tools;34.0.0`, `platforms;android-34`), and `adb` are installed (macOS: `brew install --cask temurin android-commandlinetools android-platform-tools`).
  2. Run `./build.sh` once to generate `config.properties`, populate `city` and `tmdb_key` (and optional settings), then run `./build.sh` again to build `FreeMyTV.apk`.
  3. Connect and install:

     ```bash
     adb connect <TV_IP>:5555
     adb install -r FreeMyTV.apk
     ```

  4. On TCL TVs, allow background autostart after every new install:

     ```bash
     adb shell "appops set io.freemytv AUTO_START allow || appops set io.freemytv APP_AUTO_START allow"
     ```

  5. On the TV, open `Free My TV -> Home Screen -> Free My TV` and accept `Allow USB debugging?` (tick `Always allow`).
- **LG webOS (webOS 3+)**:
  1. Enable Developer Mode and Key Server in LG's Developer Mode app on the TV.
  2. Build and install:

     ```bash
     python3 webos/build.py
     python3 webos/install.py <TV_IP>
     ```

  3. Renew Developer Mode every ~40 days with `python3 webos/renew.py <TV_IP>`.
- **Samsung Tizen (2015+)**:
  1. Open Apps on the TV, enter `1 2 3 4 5`, enable Developer mode, set Host PC IP, and restart the TV.
  2. Build and install (or use TizenBrew Installer with `simbasjungles/free-my-tv`):

     ```bash
     python3 tizen/build.py
     python3 tizen/install.py <TV_IP>
     ```

### 3. Configure Integrations and Customize

- Edit `config.properties` (never commit it) for `tmdb_key`, `tmdb_region`, `watchmode_key`, `plex_url`/`plex_token`, `trakt_client_id`, `home_assistant_url`/`home_assistant_entities`, `immich_server`, `theme`, `screensaver`, and `disable_assistant`.
- Send sensitive tokens (Home Assistant, Immich) over ADB into private app storage rather than baking them into the APK:

  ```bash
  python3 tools/send_key.py <TV_IP> home_assistant_token
  python3 tools/send_key.py <TV_IP> immich_api_key
  ```

- Push custom screensaver photos: `python3 tools/photos.py <TV_IP> photo1.jpg folder/`.
- Adapt brand-specific apps in `HomeMode.java` (`DEBLOAT`, `PROTECTED`) and `HomeApps.java` (`SHELF`, `LIVE_TV_APPS`), or add translations with `python3 tools/translate.py --new <lang>`.

## Gotchas

- **Keep `freemytv.keystore`**: Updates must be signed with the same keystore. If switching between a self-built APK and a GitHub release APK, revert to `Original` and uninstall first.
- **Chromecast with Google TV (Android 14)**: Port `5555` stays closed after reboot; enable Wireless debugging, run `adb pair <ip:port> <code>`, then `adb tcpip 5555`.
- **Unsupported switch devices**: Huawei HarmonyOS TVs and Kalley 43G200 must keep Free My TV as a regular app (do not switch the system home screen).
- **Safe rollback**: Always switch back via `Free My TV -> Home Screen -> Original` before uninstalling so disabled stock packages are re-enabled cleanly.
