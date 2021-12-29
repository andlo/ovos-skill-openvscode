"""
skill code-server
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

from sys import platform
from mycroft import MycroftSkill, intent_file_handler
import os
import subprocess
import signal
from shutil import copyfile


class CodeServer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.log.info("Initialize code-server...")

        if (self.settings.get("code-server installed") is not True or
                self.settings.get("code-server installed") is None):
            self.install_code()
        if not self.pid_exists(self.settings.get("code_pid")):
            self.settings["code_pid"] = None
        if (self.settings.get("auto_start") and
                self.settings.get("code_pid") is None):
            self.start_code()

    @intent_file_handler('stop.intent')
    def handle_code_stop(self, message):
        if self.stop_code():
            self.speak_dialog('code_stopped')
        else:
            self.speak_dialog('code_is_not_running')

    @intent_file_handler('start.intent')
    def handle_code_start(self, message):
        url = os.uname().nodename + ' ' + str(self.settings.get('portnum'))
        if self.start_code():
            self.speak_dialog('code_started', data={"url": url})
        else:
            self.speak_dialog('code_already_running', data={"url": url})

    @intent_file_handler('restart.intent')
    def handle_code_restart(self, message):
        url = os.uname().nodename + ' ' + str(self.settings.get('portnum'))
        self.stop_code()
        if self.start_code():
            self.speak_dialog('code_started', data={"url": url})

    def stop_code(self):
        self.log.info("Stopping code-server")
        SafePath = self.file_system.path
        try:
            os.killpg(self.settings.get("code_pid"), signal.SIGTERM)
        except Exception:
            proc = subprocess.Popen('pkill -f "code-server --host"',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid,
                                    shell=True)
            proc.wait()
        self.settings["code_pid"] = None
        return True

    def start_code(self):
        if self.settings.get("code_pid)") is None:
            self.log.info("Starting code-server")
            SafePath = self.file_system.path
            auth = ' --auth=none'
            if self.settings.get('use_password') is True:
                auth = 'password'
                os.environ['PASSWORD'] = self.settings.get('password')
            cert = ''
            if self.settings.get('use_ssl') is True:
                cert = ' --cert'
                os.environ['PASSWORD'] = self.settings.get('password')
                self.log.info('Password is ' + self.settings.get('password'))
            port = ' --port=3000'
            if self.settings.get('portnum') is not '':
                port = ' --port=' + str(self.settings.get('portnum'))
            telemetry = ' --disable-telemetry'
            if self.settings.get('telemetry') is False:
                telemetry = ''

            proc = subprocess.Popen(SafePath + '/code-server/bin/code-server' +
                                    ' --host=0.0.0.0' +
                                    port +
                                    auth +
                                    ' --user-data-dir=' + SafePath + '/user-data' +
                                    ' --extensions-dir=' + SafePath + '/extensions' +
                                    ' --config=' + SafePath + '/config.yaml' +
                                    cert +
                                    telemetry +
                                    ' --force',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid, shell=True)
            self.log.info('Code-server PID=' + str(proc.pid))
            self.settings["code_pid"] = proc.pid
            return True
        else:
            return False

    def install_code(self):
        try:
            SafePath = self.file_system.path
            # Need a nother way!!!
            file = '/opt/mycroft/skills/code-server-skill.andlo/download_code-server.sh'
            copyfile(file, SafePath + '/download_code-server.sh')

            proc = subprocess.Popen('bash ./download_code-server.sh armv7',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid, shell=True)
            proc.wait()
            proc = subprocess.Popen(SafePath + '/code-server/bin/code-server' +
                                    ' --install-extension' +
                                    ' ms-python.pythonport',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid, shell=True)
            proc.wait()
            self.log.info("Installed OK")
            self.settings['code-server installed'] = True
            self.speak_dialog('installed_OK')
            return True

        except Exception:
            self.log.info("Code is not installed - something went wrong!")
            self.settings['code installed'] = 'False'
            self.speak_dialog('installed_BAD')
            return False

    def pid_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False


def create_skill():
    return CodeServer()
