"""Update the cask from a published release, checking the downloaded ZIP hash."""

import hashlib
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


CASK = Path(__file__).resolve().parents[1] / "Casks" / "patchlook.rb"
UPSTREAM = "worldtheater/patchlook"
RELEASES = f"https://github.com/{UPSTREAM}/releases/download"
VERSION = re.compile(r'^  version "(\d+\.\d+\.\d+)"$', re.MULTILINE)
SHA256 = re.compile(r'^  sha256 "([0-9a-f]{64})"$', re.MULTILINE)


def download_sha256(url):
    # Public asset downloads do not receive the API authentication token.
    digest = hashlib.sha256()
    with urlopen(url, timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def updated_cask(text, release, hash_download=download_sha256):
    current = VERSION.search(text)
    current_hash = SHA256.search(text)
    if not current or not current_hash:
        raise ValueError("Cask version or SHA-256 is missing")
    if release.get("draft") or release.get("prerelease") or not release.get("published_at"):
        raise ValueError("Expected a published stable release")
    match = re.fullmatch(r"v(\d+\.\d+\.\d+)", release["tag_name"])
    if not match:
        raise ValueError("Expected a vMAJOR.MINOR.PATCH release tag")
    version = match[1]
    if tuple(map(int, version.split("."))) < tuple(map(int, current[1].split("."))):
        raise ValueError("Refusing to downgrade the cask")
    asset_name = f"patchlook-{version}-darwin-arm64.zip"
    assets = [asset for asset in release["assets"] if asset["name"] == asset_name]
    if len(assets) != 1:
        raise ValueError(f"Expected exactly one {asset_name} asset")
    asset = assets[0]
    url = f"{RELEASES}/v{version}/{asset_name}"
    if asset["browser_download_url"] != url:
        raise ValueError("Unexpected asset download URL")
    digest = re.fullmatch(r"sha256:([0-9a-f]{64})", asset.get("digest") or "")
    if not digest:
        raise ValueError("Release asset is missing its SHA-256 digest")
    sha256 = digest[1]
    if version == current[1]:
        if sha256 != current_hash[1]:
            raise ValueError("Existing release checksum changed; review it manually")
        return text
    if hash_download(url) != sha256:
        raise ValueError("Downloaded ZIP does not match the release SHA-256")
    text = VERSION.sub(f'  version "{version}"', text, count=1)
    return SHA256.sub(f'  sha256 "{sha256}"', text, count=1)


def main():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "patchlook-homebrew-tap"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{UPSTREAM}/releases/latest", headers=headers)
    with urlopen(request, timeout=30) as response:
        release = json.load(response)
    old = CASK.read_text()
    new = updated_cask(old, release)
    if new != old:
        CASK.write_text(new)
        print(f'Updated Patchlook to {release["tag_name"]}')
    else:
        print(f'Patchlook {release["tag_name"]} is already current')


if __name__ == "__main__":
    main()
