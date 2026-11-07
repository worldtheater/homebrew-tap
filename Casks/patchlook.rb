cask "patchlook" do
  version "0.1.8"
  sha256 "5ac6b41b00fd0bdf74e5a05b99788b262cd4f5acc46548cd24da105e64cd0b35"

  url "https://github.com/worldtheater/patchlook/releases/download/v#{version}/patchlook-#{version}-darwin-arm64.zip"
  name "Patchlook"
  desc "Native Git diff and history viewer"
  homepage "https://github.com/worldtheater/patchlook"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on formula: "git"
  depends_on macos: :sequoia

  app "Patchlook.app"

  zap trash: "~/Library/Application Support/patchlook"
end
