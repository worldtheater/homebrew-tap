import copy
import unittest
from unittest.mock import Mock

from update import UPSTREAM, updated_cask


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.old_hash = "a" * 64
        self.new_hash = "b" * 64
        self.text = f'cask "patchlook" do\n  version "0.1.6"\n  sha256 "{self.old_hash}"\nend\n'
        self.release = {
            "tag_name": "v0.1.7",
            "draft": False,
            "prerelease": False,
            "published_at": "2026-11-03T00:00:00Z",
            "assets": [{
                "name": "patchlook-0.1.7-darwin-arm64.dmg",
                "browser_download_url": f"https://github.com/{UPSTREAM}/releases/download/v0.1.7/patchlook-0.1.7-darwin-arm64.dmg",
                "digest": f"sha256:{self.new_hash}",
            }],
        }
        self.download = Mock(return_value=self.new_hash)

    def test_update_verifies_download_and_preserves_other_fields(self):
        result = updated_cask(self.text, self.release, self.download)
        self.assertEqual(result, self.text.replace('"0.1.6"', '"0.1.7"').replace(self.old_hash, self.new_hash))
        self.download.assert_called_once_with(self.release["assets"][0]["browser_download_url"])

    def test_current_release_is_idempotent_without_downloading(self):
        current = self.text.replace('"0.1.6"', '"0.1.7"').replace(self.old_hash, self.new_hash)
        self.assertEqual(updated_cask(current, self.release, self.download), current)
        self.download.assert_not_called()

    def test_changed_checksum_for_existing_release_requires_review(self):
        current = self.text.replace('"0.1.6"', '"0.1.7"')
        with self.assertRaisesRegex(ValueError, "checksum changed"):
            updated_cask(current, self.release, self.download)
        self.download.assert_not_called()

    def test_invalid_releases_are_rejected_before_downloading(self):
        cases = [
            {"draft": True}, {"prerelease": True}, {"published_at": None},
            {"tag_name": "v0.1.7-rc.1"}, {"tag_name": "v0.1.5"}, {"assets": []},
        ]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                updated_cask(self.text, self.release | changes, self.download)
        self.download.assert_not_called()

    def test_invalid_asset_url_or_digest_is_rejected(self):
        for changes in ({"browser_download_url": "https://example.com/app.dmg"}, {"digest": None}):
            release = copy.deepcopy(self.release)
            release["assets"][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                updated_cask(self.text, release, self.download)
        self.download.assert_not_called()

    def test_corrupted_download_is_rejected(self):
        self.download.return_value = self.old_hash
        with self.assertRaisesRegex(ValueError, "does not match"):
            updated_cask(self.text, self.release, self.download)


if __name__ == "__main__":
    unittest.main()
