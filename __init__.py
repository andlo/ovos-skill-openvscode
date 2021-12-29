from mycroft import MycroftSkill, intent_file_handler
import requests, json
import platform
import tarfile
import os
import subprocess
import signal

class OpenvscodeServer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('server.openvscode.intent')
    def handle_server_openvscode(self, message):
        self.speak_dialog('server.openvscode')


    def initialize(self):
        if (self.settings.get("vscode_installed") is not True or
                self.settings.get("vscode_installed") is None):
            self.install_vscode()
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
        url = os.uname().nodename + ' ' + str(self.settings.get('portnum'))
        if self.start_vscode():
            self.speak_dialog('vscode_started', data={"url": url})
        else:
            self.speak_dialog('vscode_already_running', data={"url": url})

    @intent_file_handler('restart.intent')
    def handle_vscode_restart(self, message):
        url = os.uname().nodename + ' ' + str(self.settings.get('portnum'))
        self.stop_vscode()
        if self.start_vscode():
            self.speak_dialog('code_started', data={"url": url})

    def stop_vscode(self):
        self.log.info("Stopping vscode")
        SafePath = self.file_system.path
        try:
            os.killpg(self.settings.get("vscode_pid"), signal.SIGTERM)
        except Exception:
            proc = subprocess.Popen('pkill -f "XXX"',
                                    cwd=SafePath,
                                    preexec_fn=os.setsid,
                                    shell=True)
            proc.wait()
        self.settings["code_pid"] = None
        return True

    def start_vscode(self):
        if self.settings.get("code_pid)") is None:
            self.log.info("Starting code-server")
            SafePath = self.file_system.path
            #port = ' --port ' + str(self.settings.get('portnum'))
            port = ' --port 3000'
            #auth = ' --connectionToken ' + self.settings.get('token')
            auth = ' --connection-token 1234'

            proc = subprocess.Popen(SafePath + '/openvscode-server/server.sh' +
                                    ' --host 0.0.0.0' +
                                    port +
                                    auth,
                                    cwd=SafePath,
                                    preexec_fn=os.setsid, shell=True)
            self.log.info('VSCode-server PID=' + str(proc.pid))
            #url = 'http://' + os.uname().nodename + ':' + str(self.settings.get('portnum') + '?tkn=' +  + self.settings.get('token'))
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

            for asset in assets:
                if 'armhf' in asset["name"]: 
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
            self.log.info("Installed OK")
            self.settings['vscode_installed'] = True
            #self.settings['vscode_version'] = data["name"]
            return True


        except Exception:
            self.log.info("VSCode is not installed - something went wrong!")
            self.settings['vscode_installed'] = False
            self.speak_dialog('installed_BAD')
            return False

    def pid_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

def create_skill():
    return OpenvscodeServer()

