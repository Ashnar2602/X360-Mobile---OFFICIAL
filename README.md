# X360 Mobile — Xbox 360 Emulator for Android

<p align="center">
  <img src="https://x360mobile.com/logo.png" alt="X360 Mobile logo" width="180"/>
</p>

<p align="center">
  <b>Experimental ARM64 Xbox 360 emulation for Android with a Vulkan renderer.</b>
</p>

<p align="center">
  <a href="https://www.x360mobile.com"><b>Official website: www.x360mobile.com</b></a>
</p>

<p align="center">
  <b>English</b> · <a href="README.it.md">Italiano</a> ·
  <a href="README.de.md">Deutsch</a> · <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

> [!IMPORTANT]
> This is the public distribution repository. It contains official signed APK
> releases, release notes, update metadata and public documentation. The active
> emulator source tree is maintained separately and is not published here.

## About the project

X360 Mobile is an experimental Android port whose current ARM64 core combines
components and behavior from the Xenia EDGE and Xenia Canary development
lines, together with Android-specific execution, graphics, input, storage and
interface work. It is not affiliated with Microsoft, Xbox or the Xenia project.

Compatibility and performance vary significantly by game, device, GPU driver
and configuration. A title booting does not imply that it is fully playable.

## Main features

- ARM64 Android execution core and Vulkan graphics backend.
- Controller-first library and in-game interface with touch support.
- Physical controller support plus configurable touch controls and haptics.
- Optional X360 Companion app for local wireless P2-P4 controllers.
- Per-game settings, custom cVars and recommended configuration profiles.
- GamerTags, profiles, saves, installed content, title updates and DLC tools.
- Game discovery for ISO/XISO, XEX, extracted `default.xex` directories, ZAR
  and recognized XBLA content layouts.
- Title-ID-based metadata, cover caching and compatibility information.
- External front-end launching and Android document-provider integration.
- Signed in-app updates with public, prerelease and maintenance channels.

## Requirements

| Component | Requirement |
|---|---|
| Operating system | Android 11 / API 30 or newer |
| CPU / ABI | 64-bit ARM device (`arm64-v8a`) |
| Graphics | Vulkan-capable GPU and working Vulkan driver |
| Memory | 8 GB RAM or more recommended for demanding titles |
| Performance | A recent high-end mobile SoC is strongly recommended |

Adreno devices are the most extensively tested. Mali and Xclipse devices are
supported by the Android backend, but game and driver compatibility may differ.
Custom Vulkan drivers are optional and are only applicable to compatible
devices; they may improve one title and regress or crash another.

## Install and update

1. Download the latest public APK from [GitHub Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases).
2. Confirm that the asset is named `x360-mobile-{version}.apk` and comes from
   this repository.
3. Allow installation from this source when Android requests it.
4. Complete the first-run wizard and select a folder containing games you own
   and have dumped legally.

The app checks this repository's `update-manifest.json` and downloads an
eligible APK directly. Before installation it verifies package identity,
version, size, SHA-256 and signing identity. Public releases are offered by
default; Alpha, Preview and Release Candidate builds require the prerelease
option. Hotfix, Revision and Repack suffixes identify maintenance packages.

Release maintainers must follow [VERSIONING.md](VERSIONING.md). A GitHub release
is not visible to the updater until the manifest workflow has completed
successfully.

## X360 Companion

The same public release may also include `x360-companion-{version}.apk` for
**X360 Companion** (`emu.x360mobile.controller`). It is a separate optional
application for using nearby Android phones as local P2-P4 controllers through
LAN or paired Bluetooth. It does not replace the emulator APK or share its app
data. Pairing, trusted hosts and remote-controller permissions are configured
from X360 Mobile under **Input > Remote controllers**.

## Supported game sources

The library can discover `.iso`/`.xiso`, `.xex`, `.zar`, extracted games with a
readable `default.xex`, and supported XBLA directory layouts. Support for a
container format does not guarantee compatibility with every title. Stripped
ISO images are recommended when created from a legally owned dump.

## Compatibility and issue reports

Use the [compatibility website](https://www.x360mobile.com) for current title
results. Do not rely on fixed compatibility percentages in old announcements:
results evolve with app versions, drivers and hardware.

Before opening an [issue](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues),
search existing reports and include the app version, game and Title ID, device,
SoC/GPU, Android version, selected Vulkan driver, game format and a concise
reproduction description. Never upload games, encryption keys or copyrighted
console content.

## Legal notice

- Xbox 360 and Xbox are trademarks of Microsoft Corporation.
- X360 Mobile is not affiliated with, authorized, sponsored or endorsed by
  Microsoft, Xbox or the Xenia project.
- The app does not provide games, console system software or copyrighted
  content. Users must supply their own legally obtained dumps.
- Emulation is experimental; use the software and custom drivers at your own
  risk.

<p align="center">© 2026 X360 Mobile Team · <a href="https://www.x360mobile.com">www.x360mobile.com</a></p>
