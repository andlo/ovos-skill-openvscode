# <img src='vscode.png' card_color='#40DBB0' width='50' style='vertical-align:bottom'/> Code-Server
Run VS Code on your Mycroft device and access it in a browser.

## About
This skill installs code-server on your Mycroft device. Code-server is VSCode in a browser and great for 
for making skills and programs. This skill, sets everything up for you.   
Code-server integrate to Github, and tools like mycroft-msm and mycroft-msk directly from the integrated 
shell.


## How to install
The skill isnt yet in the mycroft market.

mycroft-msm install https://github.com/andlo/code-server-skill.git

Skill will then install VScode. During installation it will download precompiled package and extract
it. Machine platforms currently supportet is armv7, arm64 and amd64.

After installation, there should be a log info saying "Installed code-server OK." and Mycroft should tell 
you by voice that he has installed the skill.
You can then open a web-browser and go to http://device:3000 where device is the hostname of the device.
If your Mycroft device is picroft the hostname proberly is picroft. 

There are some settings that kan be set on skill setting page on https://home.mycroft.ai/ 


```
THIRD-PARTY SOFTWARE NOTICES AND INFORMATION

1.  Microsoft/vscode version 1.47.0 (https://github.com/Microsoft/vscode)
    MIT License 

2.  Coder/code-server (https://github.com/coder/code-server)
    MIT License 
``` 

## Examples
* "Run code server"
* "End code server"
* "Restart code server"

## Credits
Andreas Lorensen (@andlo)

## Category
**Productivity**

## Tags
#vscode
#editor
#dev
