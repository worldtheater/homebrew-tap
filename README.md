# Homebrew Tap

Install [Patchlook](https://github.com/worldtheater/patchlook), a native Git diff and history viewer, with Homebrew.

Requires Apple Silicon and macOS 15 (Sequoia) or later. Git is installed as a dependency. The cask uses the signed and notarized ZIP from the official GitHub Release.

## Install

```sh
brew install --cask worldtheater/tap/patchlook
```

If you previously installed Patchlook manually, quit the app and move the existing `/Applications/Patchlook.app` to the Trash before installing with Homebrew. Your preferences are kept.

## Update

```sh
brew update
brew upgrade --cask patchlook
```

## Uninstall

```sh
brew uninstall --cask patchlook
```

To also remove Patchlook's preferences, use `brew uninstall --cask --zap patchlook` instead. Neither command removes your repositories.

## Maintenance

The **Update Patchlook** workflow checks for a new published stable release every six hours and can also be run manually from GitHub Actions. It verifies the downloaded ZIP against GitHub's SHA-256 digest, validates the cask and installation on macOS, then commits the update. Drafts and prereleases are excluded. It uses this repository's built-in `GITHUB_TOKEN`; no additional secret is required.

For a manual update, run `python3 scripts/update.py`, review the diff, and commit it. Run updater tests with `python3 -m unittest discover -s scripts`.

GitHub may pause scheduled workflows in public repositories after 60 days without activity. Re-enable **Update Patchlook** in Actions if needed.

App issues: [worldtheater/patchlook](https://github.com/worldtheater/patchlook/issues). Installation issues: [this tap](https://github.com/worldtheater/homebrew-tap/issues).
