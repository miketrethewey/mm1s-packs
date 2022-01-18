import common
import distutils.dir_util     # for copying trees
import json
import os                     # for env vars
import re
import stat                   # for file stats
import subprocess             # do stuff at the shell level
import ssl
import urllib.request
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
      with(open(os.path.join("commit.txt"), "w")) as commit:
        commit.write("Updating Repository:" + "\n")
        commit.write("\n")
        for packManifestURL in repoManifestJSON["packages"]:
          #  read each package from manifest
          #   get package manifest from master branch
          context = ssl._create_unverified_context()
          packageReq = urllib.request.urlopen(packManifestURL, context=context)
          packageJSON = json.loads(packageReq.read().decode("utf-8"))
          commit.write("Name: " + packageJSON["name"] + "\n")
          commit.write("By:   " + packageJSON["author"] + "\n")
          commit.write("URL:  " + packManifestURL + "\n")

          #   get latest release from package
          repoinfo = re.match('http(?:s?)\:\/\/(?:[^\.]*)(?:\.?)(?:[^\.]*)(?:\.?)(?:[^\/]*)(?:\/)([^\/]*)(?:\/)([^\/]*)', packManifestURL)
          user = repoinfo.group(1)
          repo = repoinfo.group(2)
          apiURL = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
          apiReq = urllib.request.urlopen(apiURL, context=context)
          apiRes = json.loads(apiReq.read().decode("utf-8"))

          #   get asset url
          #   set link for package as asset url
          packageJSON["link"] = apiRes["assets"][0]["browser_download_url"]
          commit.write("ZIP:  " + packageJSON["link"] + "\n")
          commit.write("\n")

          #   update other stuff
          for key in ["uid", "version"]:
            packageJSON[key] = packageJSON[f"package_{key}"]
            del packageJSON[f"package_{key}"]
          repoRepositoryJSON["packages"].append(packageJSON)

      repoRepositoryFile.seek(0)
      repoRepositoryFile.write(json.dumps(repoRepositoryJSON, indent=2))
      repoRepositoryFile.truncate()

def main():
  prepare_repository()

if __name__ == "__main__":
  main()
else:
  raise AssertionError("Script improperly used as import!")
