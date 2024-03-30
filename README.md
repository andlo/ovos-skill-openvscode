# <img src='favicon.ico' card_color='#40DBB0' width='50'/> OpenVSCode-Server
Run VS Code on your Mycroft device and access it in a browser.


## About
This skill installs openVScode-server on your OPenvoiceOS device. OpenVSCode-server is VSCode in a browser and great
for making skills and programs. This skill, sets everything up for you.   
OpenVSCode-server integrate fine with Github, and tools like from the integrated 
shell.

## How to install
The skill isnt yet in the mycroft market.

pip install https://github.com/andlo/ovos-skill-openvscode.git

This will install the skill, and first thing the skil does, is installing OpenVScode-server. During this installation
it will download precompiled package and extract it. 

The skille should install and work on any arm and x86 platform running OVOS 

After installation, there should be a log info saying "OpenVSCode-server installed OK" and OVOS should tell 
you by voice that he has installed the skill.
You can then open a web-browser and go to http://<device>:<port>/?tkn=<token> where <device> is the hostname of the
device, port is the portnumber (standard 3000) and token is accestoken (standard 1234).

Example:
http://ovso.local:3000/?tkn=1234

There are some settings that kan be set in the skills settings under ~/.config/mycroft/skills/ovos-skill-openvscode.andlo in settings.json.

```json{
    "auto_start": true,
    "portnum": 3000,
    "token": "1234"
}```

On evry startup of the devie, the skill checks for new updates and if there is an update it will be updated. So 
OpenVSCode should always be latest versrion. You can force an update check and update by saying "update VS code" 


```
THIRD-PARTY SOFTWARE NOTICES AND INFORMATION

1.  Microsoft/vscode (https://github.com/Microsoft/vscode)
    MIT License 

2.  gitpod-io/openvscode-server (https://github.com/gitpod-io/openvscode-server)
    MIT License 
``` 

## Examples
* "Run VS code server"
* "End VS code server"
* "Restart VS code server"

## Credits
Andreas Lorensen (@andlo)

## Category
**Productivity**

## Tags
#vscode
#editor
#dev
