import common
import distutils.dir_util     # for copying trees
import json
import os                     # for env vars
import stat                   # for file stats
import subprocess             # do stuff at the shell level
from shutil import copy, make_archive, move, rmtree  # file manipulation

def prepare_repository():
  # open ../../meta/manifests/manifest.json for reading
  with(open(os.path.join("resources", "app", "meta", "manifests", "manifest.json"), "r")) as repoManifestFile:
    repoManifestJSON = json.load(repoManifestFile)
    # open ../../repository.json for writing
    with(open(os.path.join("repository.json"), "w")) as repoRepositoryFile:
      # write name from manifest to repository
      repoRepositoryJSON = {
        "name": repoManifestJSON["name"],
        "packages": []
      }
      for packManifestURL in repoManifestJSON["packages"]:
        #  read each package from manifest
        #   get package manifest from master branch
        print(packManifestURL)
        packageJSON = {}
        #   get latest release from package
        user = "miketrethewey"
        repo = "averge_pack_mm1"
        print("https://api.github.com/repos/%s/%s/releases/latest" % (user, repo))
        apiRes = {
          "assets": [
            {
              "browser_download_url": "https://github.com/miketrethewey/averge_pack_mm1/releases/download/v1.0.33/averge_pack_mm1.zip"
            }
          ]
        }
        #   get asset url
        print(apiRes["assets"][0]["browser_download_url"])
        #   set link for package as asset url
        packageJSON["link"] = apiRes["assets"][0]["browser_download_url"]
        repoRepositoryJSON["packages"].push(packageJSON)
      repoRepositoryFile.seek(0)
      repoRepositoryFile.write(json.dumps(repoRepositoryJSON, indent=2))
      repoRepositoryFile.truncate()

def main():
  prepare_repository()

if __name__ == "__main__":
  main()
else:
  raise AssertionError("Script improperly used as import!")
