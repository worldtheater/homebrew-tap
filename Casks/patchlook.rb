cask "patchlook" do
  version "0.1.6"
  sha256 "568f9cef7d9d22497cf4982090883dba37ad3da76b0389b49e966461c57bf0b1"

  url "https://github.com/worldtheater/patchlook/releases/download/v#{version}/patchlook-#{version}-darwin-arm64.dmg"
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
