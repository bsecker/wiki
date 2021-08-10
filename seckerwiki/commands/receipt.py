import os

from PyInquirer import prompt

def receipt(cfg, args):
    # Change working dir to wiki root
    os.chdir(cfg['wiki-root'])
    options = [
        {
            'type': 'input',
            'message': 'enter product name',
            'name': 'name'
        },
        {
            'type': 'input',
            'message': 'enter date bought',
            'name': 'bought'
        }
    ]

    answers = prompt(options)

    # TODO make a popup here choosing the receipt fil