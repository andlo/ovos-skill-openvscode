# <img src='favicon.ico' card_color='#40DBB0' width='50'/> OpenVSCode-Server
Run VS Code on your Mycroft device and access it in a browser.


## About
This skill installs openVScode-server on your Mycroft device. OpenVSCode-server is VSCode in a browser and great
for making skills and programs. This skill, sets everything up for you.   
OpenVSCode-server integrate fine with Github, and tools like mycroft-msm and mycroft-msk directly from the integrated 
shell.

## How to install
The skill isnt yet in the mycroft market.

mycroft-msm install https://github.com/andlo/openvscode-server-skill.git

this will install the skill, and first thin the skil does is installing OpenVScode-server. During this installation
it will download precompiled package and extract it. 

The skille is made for picroft, but should install work on any arm and x86 platform running linux 

After installation, there should be a log info saying "OpenVSCode-server installed OK" and Mycroft should tell 
you by voice that he has installed the skill.
You can then open a web-browser and go to http://<device>:<port>/?tkn=<token> where <device> is the hostname of the
device, port is the portnumber (standard 3000) and token is accestoken (standard 1234).

If your Mycroft device is picroft the hostname proberly is picroft so you could access it with this url
http://picroft:3000/?tkn=1234

There are some settings that kan be set on skill setting page on https://home.mycroft.ai/ which is portnumner, 
access token and if VSCode-server should start when device starts.

On evry startup of the devie, the skill checks for new updates and if there is an update it will be updated. So 
OpenVSCode should always be latest versrion. You can force an update check and update by saying "update VS code" 


```
THIRD-PARTY SOFTWARE NOTICES AND INFORMATION

1.  Microsoft/vscode version 1.47.0 (https://github.com/Microsoft/vscode)
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
