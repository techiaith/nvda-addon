# coding: utf-8

# Copyright (c) 2023 Musharraf Omer
# This file is covered by the GNU General Public License.

import config
from io import StringIO
from configobj import ConfigObj

_configSpec = """[voices]
[[__many__]]
variant = string(default=None)
speaker = string(default=None)
noise_scale = integer(default=50, min=0, max=100)
length_scale = integer(default=50, min=0, max=100)
noise_w = integer(default=50, min=0, max=100)

[lang]
[[__many__]]
voice = string(default=None)
"""


class TechiaithConfigManager:
    """Config manager for Techiaith TTS."""

    def __init__(self):
        if not config.conf["speech"].isSet("techiaith_tts"):
            config.conf["speech"]["techiaith_tts"] = {}
        confspec = ConfigObj(StringIO(_configSpec), list_values=False, encoding="UTF-8")
        config.conf["speech"]["techiaith_tts"].spec.update(confspec)

    def __contains__(self, key):
        return key in config.conf["speech"]["techiaith_tts"]

    def __getitem__(self, key):
        return config.conf["speech"]["techiaith_tts"][key]

    def __setitem__(self, key, value):
        config.conf["speech"]["techiaith_tts"][key] = value

    def setdefault(self, key, value):
        if key not in config.conf["speech"]["techiaith_tts"]:
            config.conf["speech"]["techiaith_tts"][key] = value
        return config.conf["speech"]["techiaith_tts"][key]


TechiaithConfig = TechiaithConfigManager()
