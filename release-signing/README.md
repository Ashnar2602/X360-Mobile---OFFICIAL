# X360 Mobile release signing

Official APK files for the current X360 Mobile application ID
`emu.x360mobile.com` are signed with the release identity whose public
certificate is published in this directory. This repository never contains the
private key, passwords or signing lineage.

SHA-256 certificate fingerprint:

`4A:1E:7E:3F:62:65:D2:27:9A:59:E4:25:7C:67:4C:3C:4A:31:3E:A6:D8:A6:9D:30:B8:06:A6:FF:3D:F4:66:37`

The in-app updater verifies the downloaded package ID, version, size, SHA-256
and signing identity before asking Android to install it. A checksum proves
file integrity against the manifest; it does not replace Android signature
verification.

Only APK assets published by this repository and matching this signing identity
should be treated as official. The certificate file is public verification
material and cannot be used to sign another APK.

Legacy 0.5.x APKs use a different application ID and cannot be updated in place
to the current package. They are intentionally absent from
`update-manifest.json`, whose update line begins with the 0.6.x application.

Release naming and manifest publication rules are documented in
[`../VERSIONING.md`](../VERSIONING.md).
