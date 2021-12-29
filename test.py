import requests, json
import platform
import tarfile
import os


url = requests.get("https://api.github.com/repos/gitpod-io/openvscode-server/releases/latest")
text = url.text
data = json.loads(text)
assets = data["assets"]

for asset in assets:
    if 'armhf' in asset["name"]: 
        print(asset["name"])
        #print(asset["browser_download_url"])
        r = requests.get(asset["browser_download_url"])
        f = open(asset["name"], "wb")
        f.write(r.content)
        f.close
        f = tarfile.open(asset["name"])
        f.extractall('./')
        f.close()
        d = asset["name"].strip('.tar.gz')
        os.rename(d, 'openvscode-server')
        os.remove(asset["name"])


#print(platform.machine())