# X360 Mobile release versioning

This repository distributes signed APKs and generates the manifest consumed by
the in-app updater. Release names are not free-form.

## Canonical names

| Purpose | `versionName` and asset suffix | GitHub prerelease |
|---|---|---|
| Alpha Test | `X.Y.Z-alpha.N` | Yes |
| Preview | `X.Y.Z-preview.N` | Yes |
| Release Candidate | `X.Y.Z-rc.N` | Yes |
| Initial Public | `X.Y.Z` | No |
| Maintenance | append `.hotfix.N`, `.revision.N`, or `.repack.N` to an explicit channel | Inherit channel |

Examples are `0.6.2-public.hotfix.1`, `0.6.2-public.revision.2` and
`0.6.3-rc.2.hotfix.3`. `public.N` is accepted only as legacy input and
normalizes to `public.revision.N`.

Hotfix, Revision and Repack describe the reason for a package. They share one
maintenance counter per base version and channel. If Hotfix 1 has shipped, the
next maintenance package is 2 even when it is classified as a Revision.

Emulator tags are always `v{versionName}`. A combined emulator/Companion
release contains exactly two APK assets: `x360-mobile-{versionName}.apk` and
`x360-companion-{companionVersion}.apk`. The Companion has its own package and
independent update feed, but is intentionally published in the same GitHub
Release as the matching emulator build.

## Android `versionCode`

Every distributed APK must use a strictly increasing `versionCode`:

```text
major * 100000000 + minor * 1000000 + patch * 10000 + stage * 1000 + publicationSequence
```

Stages are Alpha `0`, Preview `1`, RC `2` and Public `9`. The initial Public
has publication sequence zero. A Public maintenance sequence matches its
shared maintenance number. A normal prerelease sequence matches its channel
number. A prerelease maintenance package needs a later publication sequence
than the channel build it replaces. `tools/x360_versioning.py` is authoritative
and the workflow rejects mismatches.

## Optional updater policy

One invisible JSON comment may be added to GitHub release notes:

```html
<!-- x360-update: {"mandatory":false,"security":false,"blockedVersionCodes":[],"supersedes":"0.6.2","rolloutPercentage":100,"minSourceVersionCode":0,"maxSourceVersionCode":0} -->
```

All fields are optional. Unknown fields fail publication. Source ranges are
inclusive and zero means unbounded. Mandatory updates and updates required by a
blocked installed `versionCode` cannot be skipped or postponed and bypass a
staged rollout, so use these controls only for a verified recovery or security
requirement.

## Publication guarantees

`.github/workflows/publish-update-manifest.yml` verifies both APK filenames,
package IDs, versions, host channel and GitHub prerelease flag. It then
calculates size and SHA-256 and generates schema 2 of `update-manifest.json`
for X360 Mobile plus `controller-update-manifest.json` for the Companion.

A version is immutable: rerunning with the identical APK is a no-op, while an
APK with different bytes under the same version is rejected. The feed retains
the newest Public and prerelease entries plus the newest legacy-readable bridge
for each class.

The 0.6.1 updater does not understand Alpha or structured double suffixes. The
first release carrying the new parser must therefore use a legacy-readable
name, preferably a new plain `X.Y.Z` Public release. Do not remove the bridge
entry while legacy installations remain supported.

Run the public tooling tests before changing this contract:

```powershell
python -m unittest discover -s tools/tests -v
```
