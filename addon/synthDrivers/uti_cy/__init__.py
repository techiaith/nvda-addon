from collections import OrderedDict
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
from speech.commands import IndexCommand, VolumeCommand
import nvwave
import config
import urllib.parse
from logHandler import log


class SynthDriver(SynthDriver):
    """A dummy synth driver used to disable speech in NVDA.
    """
    name = "uti_cy"
    # Translators: Description for a speech synthesizer.
    description = "uti_cy"

    @classmethod
    def check(cls):
        return True

    supportedSettings = (SynthDriver.VoiceSetting(), SynthDriver.VolumeSetting())
    supportedCommands = {
        IndexCommand,
        VolumeCommand,
    }

    availableVoices = OrderedDict({name: VoiceInfo(name, description)})
    supportedNotifications = {synthIndexReached, synthDoneSpeaking}

    def speak(self, speechSequence):
        self.lastIndex = None
        text = ""
        for item in speechSequence:
            if isinstance(item, IndexCommand):
                self.lastIndex = item.index
            elif isinstance(item, str):
                text = text + item
        url = 'https://api.techiaith.org/coqui-tts/api/v1?testun=' + urllib.parse.quote(text,
                                                                                        safe='') + '&siaradwr=gwyrw-gogleddol-pro&api_key='
        nvwave.playWaveFile(urllib.request.urlopen(url))

    def cancel(self):
        self.lastIndex = None

    def _get_voice(self):
        return self.name
