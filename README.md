# X360 Mobile - Xbox 360 Emulator for Android

<p align="center">
  <img src="https://x360mobile.com/logo.png" alt="X360 Mobile Logo" width="180" style="border-radius: 20%;"/>
</p>

<p align="center">
  <b>An experimental native Xbox 360 emulator for Android, natively based on Xenia Canary.</b>
</p>

<p align="center">
  <a href="https://www.x360mobile.com"><b>Official Website: www.x360mobile.com</b></a>
</p>

<p align="center">
  Choose Language / Scegli la lingua / Sprache wählen / Choisir la langue / Seleccionar idioma:
  <br>
  <b>English</b> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a>
</p>

---

Welcome to the official repository of **X360 Mobile**, an experimental, native Xbox 360 emulator built specifically for the Android platform. Developed using modern ARM64 and Vulkan 1.3 technologies, X360 Mobile is the **pioneer in natively utilizing the highly acclaimed Xenia Canary core on Android**, delivering advanced optimization and high performance directly to your high-end mobile devices.

> [!NOTE]
> **Repository Purpose:** 
> To safeguard the codebase and maintain proprietary performance enhancements, **X360 Mobile is closed-source**. This official repository does not contain the emulator's source code. Instead, it serves as the **official version archive and primary distribution platform** for releasing APK builds, managing compatibility issues, and sharing user guides.

---

## Key Features

* **Native Xenia Canary Foundation:** The very first Android emulator natively designed around Xenia Canary from inception, rather than migrating from Xenia Master, ensuring superior architecture and performance.
* **Modern Vulkan Backend:** Leverages Vulkan 1.3 to deliver optimal hardware utilization, high frame rates, and low overhead.
* **Custom Touch Overlay:** Fully customizable virtual gamepads with haptic feedback, fluid analog response, and tailored layouts for any screen size.
* **Physical Controller Support:** Seamless plug-and-play support for physical controllers via Bluetooth or USB-OTG (including Xbox Series X|S, DualSense, DualShock 4, and major mobile controllers).
* **Game-Specific Profiles:** Adjust resolutions, shader compilation options, and memory constraints individually per game to squeeze every bit of power from your device.
* **Performance Enhancements:** Integrated translation of PowerPC assembly to ARM64 instructions with specific micro-optimizations for Snapdragon and Dimensity chipsets.

---

## System Requirements

Xbox 360 emulation is an experimental and computationally intense process requiring sophisticated hardware translation. Please check the requirements below to understand your device's expected performance.

| Specification | Minimum Requirements | Recommended (For Playable Speeds) |
| :--- | :--- | :--- |
| **Operating System** | Android 11 (64-bit) | Android 13 or newer (64-bit) |
| **Processor & GPU** | Qualcomm Snapdragon with Adreno GPU (600/700/800 series) | High-end Qualcomm Snapdragon (Snapdragon 8 Gen 1 or higher recommended) |
| **RAM (Memory)** | 6 GB RAM | 8 GB - 12 GB RAM (or higher) |
| **Storage (Speed)** | High-speed storage (UFS 3.1 or superior recommended) | Ultra-fast UFS 3.1/4.0 storage |

> [!WARNING]
> Devices utilizing processors with Mali GPUs, Samsung's Xclipse GPUs (AMD RDNA-based), older Adreno GPUs (prior to the 600 series), or entry-level/low-end chipsets will experience severe performance limitations, visual glitches, heavy thermal throttling, or crashes. A modern Qualcomm Snapdragon processor with an Adreno GPU is highly recommended for optimal results.

---

## Quick Start Guide

Release maintainers must follow the canonical naming, updater-policy and
legacy-bridge rules in [VERSIONING.md](VERSIONING.md).

1. **Download the APK:** Head over to our [Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases) section and download the latest stable `.apk` package.
2. **Enable Unknown Sources:** If prompted, allow your web browser or file manager to install applications from unknown sources in your Android security settings.
3. **Install and Launch:** Install the downloaded APK file and launch **X360 Mobile**.
4. **Configure Directories:** Create a dedicated directory on your device's internal or external storage (e.g., `/Emulation/Xbox360/Games`) and place your legally obtained game files there.
5. **Game Formats:** The emulator officially supports `.iso`, `.xex`, and unpacked directory formats.
6. **Load & Play:** Direct the emulator to your games folder, select a game title, and start playing!

---

## Frequently Asked Questions (FAQ)

### Is X360 Mobile free?
**Yes.** X360 Mobile is free to download and use. We do not charge fees, nor do we include intrusive ads that ruin the gaming experience.

### Why is the project closed-source?
We made the choice to keep X360 Mobile closed-source to prevent fraudulent forks, malicious repackaging (e.g., injecting adware/spyware into our builds), and to protect our proprietary ARM64 conversion pipeline and compiler optimizations. We want to ensure that users receive only secure, highly optimized, and officially signed packages directly from this repository or our official website.

### Is X360 Mobile related to the desktop Xenia project?
X360 Mobile is built upon the incredible codebase of **Xenia Canary** (an open-source project for PC). We have ported, refactored, and optimized their core rendering and execution engines to run on Android. We hold the utmost respect for the original Xenia developers and aim to deliver the same high-standard experience on mobile devices.

### What games can I run right now?
Compatibility is an ongoing effort. Currently, **over 300 titles have been tested**, out of which approximately **40% are fully playable**. 

For a complete and up-to-date compatibility list, please visit our official website at [www.x360mobile.com](https://www.x360mobile.com). While classic Arcade titles, indie games, and lighter 3D games run very well, demanding AAA titles (such as *Red Dead Redemption*, *Halo 3*, or *Gears of War*) are bootable and can achieve playable speeds on the latest flagship Snapdragon processors, though they may still exhibit minor graphical bugs or frame drops.

---

## Reporting Issues

If you encounter crashes, graphical bugs, or compatibility problems:
1. Go to the [Issues](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues) section.
2. Search if the issue has already been reported.
3. If not, open a new issue using our template and include:
   * Your device model and chipset (e.g., Samsung Galaxy S23, Snapdragon 8 Gen 2).
   * Exact Android version and RAM.
   * Game title and format (.iso or .xex).
   * Detailed description of the bug and, if possible, screenshots or video clips.

---

## Legal & Disclaimers

* **Xbox 360** is a registered trademark of Microsoft Corporation. **X360 Mobile** is in no way affiliated with, authorized, sponsored, or endorsed by Microsoft Corporation, its affiliates, or subsidiaries.
* All game titles, images, and brand assets are trademarks of their respective owners.
* **X360 Mobile** does not include any game files, system software (dashboard), or copyrighted ROMs. Users are legally required to own physical copies of the games and dump them for personal, non-commercial use.
* By downloading and using this software, you agree to our terms of service and acknowledge that emulation is an experimental technology used at your own risk.

---

<p align="center">
  © 2026 X360 Mobile Team. All Rights Reserved. <br>
  For news, updates, and more, visit <a href="https://www.x360mobile.com">www.x360mobile.com</a>.
</p>
