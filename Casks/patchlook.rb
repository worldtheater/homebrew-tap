cask "patchlook" do
  version "0.1.6"
  sha256 "1f743e8ed518d9945b9cf30336f2e2deb7dfcdae796aa31770c1c17a14052ac3"

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
