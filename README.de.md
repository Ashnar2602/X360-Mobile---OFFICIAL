# X360 Mobile — Xbox-360-Emulator für Android

<p align="center"><img src="https://x360mobile.com/logo.png" alt="X360 Mobile-Logo" width="180"/></p>
<p align="center"><b>Experimentelle ARM64-Xbox-360-Emulation für Android mit Vulkan-Renderer.</b></p>
<p align="center"><a href="https://www.x360mobile.com"><b>Offizielle Website: www.x360mobile.com</b></a></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.it.md">Italiano</a> ·
  <b>Deutsch</b> · <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

> [!IMPORTANT]
> Dies ist das öffentliche Distributions-Repository. Es enthält offiziell
> signierte APK-Releases, Versionshinweise, Update-Metadaten und öffentliche
> Dokumentation. Der aktive Emulator-Quellcode wird getrennt verwaltet und hier
> nicht veröffentlicht.

## Über das Projekt

X360 Mobile ist ein experimenteller Android-Port. Sein aktueller ARM64-Core
kombiniert Komponenten und Verhaltensweisen der Entwicklungslinien Xenia EDGE
und Xenia Canary mit Android-spezifischer Arbeit an Ausführung, Grafik,
Eingabe, Speicher und Benutzeroberfläche. Es besteht keine Verbindung zu
Microsoft, Xbox oder dem Xenia-Projekt.

Kompatibilität und Leistung hängen stark von Spiel, Gerät, GPU-Treiber und
Konfiguration ab. Ein startendes Spiel ist nicht automatisch vollständig
spielbar.

## Hauptfunktionen

- ARM64-Android-Core und Vulkan-Grafikbackend.
- Controller-orientierte Bibliothek und In-Game-Oberfläche mit Touch-Support.
- Physische Controller, konfigurierbare Touch-Steuerung und Vibration.
- Spielebezogene Einstellungen, eigene cVars und empfohlene Profile.
- GamerTags, Profile, Spielstände, installierte Inhalte, Title Updates und DLC.
- Erkennung von ISO/XISO, XEX, extrahierten `default.xex`-Ordnern, ZAR und
  unterstützten XBLA-Strukturen.
- Title-ID-Metadaten, dauerhafter Cover-Cache und Kompatibilitätsstatus.
- Externe Frontends und Android Document Provider.
- Signierte Updates mit öffentlichen, Vorab- und Wartungskanälen.

## Voraussetzungen

| Komponente | Voraussetzung |
|---|---|
| Betriebssystem | Android 11 / API 30 oder neuer |
| CPU / ABI | 64-Bit-ARM-Gerät (`arm64-v8a`) |
| Grafik | Vulkan-fähige GPU mit funktionierendem Vulkan-Treiber |
| Arbeitsspeicher | Für anspruchsvolle Titel werden mindestens 8 GB empfohlen |
| Leistung | Ein aktuelles High-End-Mobil-SoC wird dringend empfohlen |

Adreno-Geräte wurden am umfangreichsten getestet. Mali und Xclipse werden vom
Android-Backend unterstützt, die Spiel- und Treiberkompatibilität kann jedoch
abweichen. Benutzerdefinierte Vulkan-Treiber sind optional und nur für
kompatible Geräte geeignet; sie können einzelne Spiele verbessern, aber andere
verschlechtern oder zum Absturz bringen.

## Installation und Updates

1. Laden Sie die neueste öffentliche APK von [GitHub Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases) herunter.
2. Prüfen Sie, dass die Datei `x360-mobile-{version}.apk` heißt und aus diesem
   Repository stammt.
3. Erlauben Sie die Installation aus dieser Quelle, wenn Android danach fragt.
4. Schließen Sie den Einrichtungsassistenten ab und wählen Sie einen Ordner mit
   legal erworbenen und selbst gesicherten Spielen.

Die App liest `update-manifest.json` aus diesem Repository und lädt geeignete
APKs direkt herunter. Vor der Installation prüft sie Paket, Version, Größe,
SHA-256 und Signaturidentität. Öffentliche Releases werden standardmäßig
angeboten; Alpha, Preview und Release Candidate erfordern die Vorabversions-
Option. Hotfix, Revision und Repack kennzeichnen Wartungspakete.

Release-Verantwortliche müssen [VERSIONING.md](VERSIONING.md) befolgen. Ein
GitHub-Release erscheint erst nach erfolgreichem Manifest-Workflow im Updater.

## Unterstützte Spielquellen

Die Bibliothek erkennt `.iso`/`.xiso`, `.xex`, `.zar`, extrahierte Spiele mit
lesbarer `default.xex` sowie unterstützte XBLA-Verzeichnisstrukturen. Die
Erkennung eines Containers garantiert nicht die Kompatibilität jedes Spiels.
Bei legal eigenen Dumps werden nach Möglichkeit verkleinerte ISO-Dateien
empfohlen.

## Kompatibilität und Fehlerberichte

Aktuelle Ergebnisse finden Sie auf der [Kompatibilitätsseite](https://www.x360mobile.com).
Feste Prozentangaben aus älteren Mitteilungen sind nicht verlässlich, da sich
Ergebnisse mit App-Version, Treiber und Hardware ändern.

Suchen Sie vor einer neuen [Issue](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues)
nach vorhandenen Meldungen. Nennen Sie App-Version, Spiel und Title ID, Gerät,
SoC/GPU, Android-Version, Vulkan-Treiber, Format und Reproduktionsschritte.
Laden Sie niemals Spiele, Schlüssel oder urheberrechtlich geschützte
Konsoleninhalte hoch.

## Rechtliche Hinweise

- Xbox 360 und Xbox sind Marken der Microsoft Corporation.
- X360 Mobile ist nicht mit Microsoft, Xbox oder dem Xenia-Projekt verbunden,
  von ihnen autorisiert, gesponsert oder unterstützt.
- Die App enthält keine Spiele, Konsolen-Systemsoftware oder geschützte Inhalte.
  Benutzer müssen eigene legal erstellte Dumps verwenden.
- Emulation ist experimentell; Nutzung der Software und benutzerdefinierter
  Treiber erfolgt auf eigenes Risiko.

<p align="center">© 2026 X360 Mobile Team · <a href="https://www.x360mobile.com">www.x360mobile.com</a></p>
