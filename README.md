# <img src='favicon.ico' card_color='#40DBB0' width='50'/> openVSCode-Server
Run VS Code on your Mycroft device and access it in a browser.


## About
This skill installs openVScode-server on your Mycroft device. OpenVSCode-server is VSCode in a browser and great for 
for making skills and programs. This skill, sets everything up for you.   
openVSCode-server integrate to Github, and tools like mycroft-msm and mycroft-msk directly from the integrated 
shell.


## How to install
The skill isnt yet in the mycroft market.

mycroft-msm install https://github.com/andlo/openvscode-server-skill.git

Skill will then install openVScode-server. During installation it will download precompiled package and extract
it. 
The skille is made for picroft, but should install work on any arm and x86 platform running linux 

After installation, there should be a log info saying "OpenVSCode-server installed OK" and Mycroft should tell 
you by voice that he has installed the skill.
You can then open a web-browser and go to http://device:3000 where device is the hostname of the device.
If your Mycroft device is picroft the hostname proberly is picroft. 

There are some settings that kan be set on skill setting page on https://home.mycroft.ai/ 

On evry devices start the skill checks for update and if here is an update it will be updated.

You can force an update check and update by saying "update VS code" 


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
