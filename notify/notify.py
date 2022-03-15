import requests
import threading
import json
import time
import argparse


def _send_discord_msg(HOOK, messageType, *args, **kw):
    discord_colors = {
        'log': 0x000000,
        'debug': 0x000000,
        'info': 0x00FF00,
        'error': 0xFF0000,
        'fatal': 0xFF0000,
        'warning': 0xFFFF00
    }
    if not HOOK:
        return

    requests.post(HOOK,
                  data=json.dumps({
                      'content': '',
                      'username': 'Github-CI',
                      'embeds': [{
                          'title': serviceName+": "+messageType,
                          'description': 'At ' +
                          time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),
                          'fields': [{
                                  'name': 'Message',
                                  'value': ' '.join(list(map(lambda x: str(x),
                                                             args)))
                          }],
                          'color': discord_colors.get(messageType, 0x000000)
                      }]
                  }), headers={'Content-Type': 'application/json'})


def send_discord_msg(HOOK, messageType, *args, **kw):
    threading.Thread(target=_send_discord_msg,
                     args=(HOOK, messageType, *args), kwargs=kw).start()


with open('secrets.json') as f:
    SECRETS = json.load(f)
DISCORD_WEBHOOK = SECRETS['discord_webhook']


parser = argparse.ArgumentParser()
parser.add_argument('--type', '-t', help='Type', default=['log'],
                    choices=['log', 'debug', 'info',
                             'error', 'fatal', 'warning'],
                    nargs=1
                    )
parser.add_argument('--message', '-m', help='Message', required=True, nargs=1)
parser.add_argument('--name', '-n', help='Service Name',
                    default=["Unknown Service"], nargs=1)
parser.add_argument('--hook', help='Hook Name',
                    required=True, nargs=1)

args = parser.parse_args()

msgType = args.type[0]
msg = args.message[0]
serviceName = args.name[0]
hookName = args.hook[0]

HOOK = DISCORD_WEBHOOK[hookName]
send_discord_msg(HOOK, msgType, msg)
