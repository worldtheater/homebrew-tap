cask "patchlook" do
  version "0.1.7"
  sha256 "990b7bf56b7c44f6bd7e43906c0f162a499213e2830e4d9577e0ef699f4d5499"

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
