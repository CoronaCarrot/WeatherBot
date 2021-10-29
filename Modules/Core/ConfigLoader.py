import json
import os
import time
from random import randint

from termcolor import colored, cprint


def configjson(self):
    if os.path.exists(os.getcwd() + "/config.json"):

        with open("./config.json") as f:
            configData = json.load(f)

    else:
        configTemplate = {
            "Token": "YOUR BOT TOKEN",
            "Prefix": "PREFIX HERE",
            "Owner": "OWNER ID HERE",
            "WeatherAPIKey": "API KEY HERE",
            "Presence": {
                "Type": "watching",
                "Message": "The Weather"
            },
            "Require Auth Code For High Security Commands": True
        }

        with open(os.getcwd() + "/config.json", "w+") as f:
            json.dump(configTemplate, f)

        print(colored("―――――――――――――――", "blue"))  # |
        print(colored("》", "blue"), "    Weather Bot    ", colored("《", "blue"))  # | Sends Bot branding to console
        print(colored("   •", "blue"), "version  0.0.1", colored("•", "blue"))  # | and sends version info
        print(colored("―――――――――――――――", "blue"))  # |
        print()
        cprint('⚙️Beginning First Boot Setup',
                'blue')  # Sends in console that the bot is beginning first time setup
        time.sleep(randint(0, 3))  # Pause For Effect
        cprint('⚙️Creating Config Files', 'blue')  # Sends in console that the bot is creating config files
        time.sleep(randint(0, 3))  # Pause For Effect
        with open("./config.json") as f:
            configData = json.load(f)
        firstboot = 1
        return firstboot, configData
