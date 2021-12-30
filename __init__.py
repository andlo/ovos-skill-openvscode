"""
skill OpenVSCode-server
Copyright (C) 2022  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill, intent_file_handler
import requests, json
import platform
import tarfile
import os
import subprocess
import signal
import shutil


class OpenvscodeServer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        if (self.settings.get("auto_start") is not True):
            self.settings["auto_start"] = True
        if (self.settings.get("portnum") is not True):
            self.settings["portnum"] = 3000
        if (self.settings.get("token") is not True):
            self.settings["token"] = "1234"
        if (self.settings.get("vscode_installed") is not True or
                self.settings.get("vscode_installed") is None):
            self.install_vscode()
        else:
            self.update_vscode()
        if not self.pid_exists(self.settings.get("vscode_pid")):
            self.settings["vscode_pid"] = None
        if (self.settings.get("auto_start") and
                self.settings.get("vscode_pid") is None):
            self.start_vscode()

    @intent_file_handler('stop.intent')
    def handle_vscode_stop(self, message):
        if self.stop_vscode():
            self.speak_dialog('vscode_stopped')
        else:
            self.speak_dialog('vscode_is_not_running')

    @intent_file_handler('start.intent')
    def handle_vscode_start(self, message):
        url = 'http://' + os.uname().nodename + ':' + str(self.settings.get('portnum')) + '?tkn=' + self.settings.get('token')
        if self.start_vscode():
            self.speak_dialog('vscode_started', data={"url": url})
        else:
            self.speak_dialog('vscode_already_running', data={"url": url})

    @intent_file_handler('restart.intent')
    def handle_vscode_restart(self, message):
        url = 'http://' + os.uname().nodename + ':' + str(self.settings.get('portnum')) + '?tkn=' + self.settings.get('token')
        self.stop_vscode()
        self.start_vscode()

    @intent_file_handler('update.intent')
    def handle_vscode_update(self, message):
        self.speak_dialog('vscode_check_for_update')
        self.update_vscode()

    def stop_vscode(self):
        self.log.info("Stopping openVSCode-server")
        SafePath = self.file_system.path
        try:
            os.killpg(self.settings.get("vscode_pid"), signal.SIGTERM)
        except Exception:
            proc = subprocess.Popen('pkill -f "server.sh --host 0.0.0.0"' +
                                    '  >/dev/null 2>/dev/null',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid,
                                    shell=True)
            proc.wait()
        self.settings["vscode_pid"] = None
        return True

    def start_vscode(self):
        if self.settings.get("vscode_pid") is None:
            self.log.info("Starting openVSCode-server")
            SafePath = self.file_system.path
            port = ' --port ' + str(self.settings.get('portnum'))
            auth = ' --connection-token ' + self.settings.get('token')
            env = {**os.environ, 'PATH': '$HOME/bin:$HOME/mycroft-core/bin:' + os.environ['PATH']}
            proc = subprocess.Popen(SafePath + '/openvscode-server/server.sh' +
                                    ' --host 0.0.0.0' +
                                    port +
                                    auth +
                                    ' >/dev/null 2>/dev/null ',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid, shell=True, executable='/bin/bash', env=env)
            self.log.info('VSCode-server PID=' + str(proc.pid))
            url = 'http://' + os.uname().nodename + ':' + str(self.settings.get('portnum')) + '?tkn=' + self.settings.get('token')
            self.log.info('To access VSCode go to ' + url)
            self.settings["vscode_pid"] = proc.pid
            return True
        else:
            return False

    def install_vscode(self):
        try:
            SafePath = self.file_system.path

            url = requests.get("https://api.github.com/repos/gitpod-io/openvscode-server/releases/latest")
            text = url.text
            data = json.loads(text)
            assets = data["assets"]
            pf = platform.machine()
            if pf == 'arm71':
                pf = 'armhf'
            if pf == 'aarch64':
                pf = 'arm64'
            if pf == 'x86_64':
                pf = 'x64'
            for asset in assets:
                if pf in asset["name"]: 
                    filename = SafePath + '/' + asset["name"]
                    r = requests.get(asset["browser_download_url"])
                    f = open(filename, "wb")
                    f.write(r.content)
                    f.close
                    f = tarfile.open(filename)
                    f.extractall(SafePath)
                    f.close()
                    
                    olddir = filename.strip('.tar.gz')
                    newdir = SafePath + '/' + 'openvscode-server'
                    os.rename(olddir, newdir)
                    os.remove(filename)
            self.log.info("OpenVSCode-server installed OK")
            self.settings['vscode_installed'] = True
            self.settings['vscode_version'] = data["name"]
            self.speak_dialog('installed_OK')
            return True


        except Exception:
            self.log.info("OpenVSCode-server is not installed - something went wrong!")
            self.settings['vscode_installed'] = False
            self.speak_dialog('installed_BAD')
            return False

    def update_vscode(self):
        try:
            self.log.info("Checking for uptate")
            SafePath = self.file_system.path
            url = requests.get("https://api.github.com/repos/gitpod-io/openvscode-server/releases/latest")
            text = url.text
            data = json.loads(text)
            current = self.settings.get("vscode_version")
            new = data["name"]
            if not current == new:
                    self.log.info("Current version is " + current)
                    self.log.info("New verson is avaible " + new)
                    self.speak_dialog('update', data={"current": current, "new": new})
                    self.log.info("Updating now" + new)
                    self.stop_vscode()
                    shutil.rmtree(SafePath + '/' + 'openvscode-server', ignore_errors=True)
                    self.settings['vscode_installed'] = False
                    self.settings['vscode_version'] = None
                    self.install_vscode()
            else:
                self.log.info("Alreddy at latest version which is " + current)
            return True
        except Exception:
             return False


    def pid_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

def create_skill():
    return OpenvscodeServer()

