from mycroft import MycroftSkill, intent_file_handler


class OpenvscodeServer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('server.openvscode.intent')
    def handle_server_openvscode(self, message):
        self.speak_dialog('server.openvscode')


def create_skill():
    return OpenvscodeServer()

