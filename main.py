from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from subprocess import Popen, PIPE
import logging
import gi
import os
import re
import subprocess
import pyperclip

logger = logging.getLogger(__name__)

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

# Set the SPECTRE_ASKPASS environment variable to use ssh-askpass
os.environ['SPECTRE_ASKPASS'] = 'ssh-askpass'

from gi.repository import Notify


class Spectre(Extension):

    def __init__(self):
        super(Spectre, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_argument()
        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name="Get a password from spectre",
                description="" if not data else 'Run "%s" in shell' % data,
                on_enter=ExtensionCustomAction(data),
            ),
        ]

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def run_command(self, command, stdin):
        if command == '':
            return stdin
        process = Popen(command.strip(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        if stderr:
            return stderr

    def on_event(self, event, extension):
        data = event.get_data() or ""
        tokens = []
        items = []
        if data == '':
            return RenderResultListAction(items)

        try:
            completed_process = subprocess.run(['spectre', data], capture_output=True, text=True, check=True)

            output = completed_process.stdout.strip()

            subprocess.run(['xclip', '-selection', 'clipboard'], input=output.encode('utf-8'))

        except subprocess.CalledProcessError as e:
            print(f"Error executing spectre command: {e}")


if __name__ == '__main__':
    Spectre().run()
