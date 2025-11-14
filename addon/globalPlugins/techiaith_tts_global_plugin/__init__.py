# coding: utf-8

# Copyright (c) 2023 Musharraf Omer
# This file is covered by the GNU General Public License.

import os
import sys

import wx

import core
import gui
import globalPluginHandler
from logHandler import log

import addonHandler

addonHandler.initTranslation()


_DIR = os.path.abspath(os.path.dirname(__file__))
_ADDON_ROOT = os.path.abspath(os.path.join(_DIR, os.pardir, os.pardir))
_TTS_MODULE_DIR = os.path.join(_ADDON_ROOT, "synthDrivers")
sys.path.insert(0, _TTS_MODULE_DIR)
from techiaith_tts import helpers
from techiaith_tts import aio
from techiaith_tts.tts_system import (
    TechiaithTextToSpeechSystem,
    TECHIAITH_VOICES_DIR,
)
sys.path.remove(_TTS_MODULE_DIR)
del _DIR, _ADDON_ROOT, _TTS_MODULE_DIR

from . import voice_download


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__auto_download_attempted = False
        self._voice_checker = lambda: wx.CallLater(3000, self._perform_voice_check)
        core.postNvdaStartup.register(self._voice_checker)

    def _perform_voice_check(self):
        """Check for Welsh voices and prompt user to download if none are installed."""
        if self.__auto_download_attempted:
            log.debug("Voice check: Auto-download already attempted, skipping.")
            return

        installed_voices = list(TechiaithTextToSpeechSystem.load_piper_voices_from_nvda_config_dir())

        log.info(f"Voice check: Found {len(installed_voices)} installed voices.")

        # Check if the correct voice files exist (not just old files)
        should_prompt_download = False

        if not installed_voices:
            should_prompt_download = True
            log.info("Voice check: No voice directories found.")
        else:
            log.info(f"Voice check: Installed voice keys: {[v.key for v in installed_voices]}")
            # Check if voice files actually exist with correct names
            voices_dir = TECHIAITH_VOICES_DIR
            log.info(f"Voice check: Voices directory: {voices_dir}")
            log.info(f"Voice check: Directory exists: {os.path.exists(voices_dir)}")

            # Verify that the expected voice files exist with correct names
            expected_voice_dir = os.path.join(voices_dir, "cy-ms-medium")
            expected_onnx_file = os.path.join(expected_voice_dir, "cy_en_GB-bu_tts.onnx")
            expected_json_file = os.path.join(expected_voice_dir, "cy_en_GB-bu_tts.onnx.json")

            if os.path.exists(expected_voice_dir):
                log.info(f"Voice check: Expected voice directory exists: {expected_voice_dir}")
                files_in_dir = os.listdir(expected_voice_dir) if os.path.isdir(expected_voice_dir) else []
                log.info(f"Voice check: Files in directory: {files_in_dir}")

                onnx_exists = os.path.exists(expected_onnx_file)
                json_exists = os.path.exists(expected_json_file)

                log.info(f"Voice check: Expected ONNX file exists ({expected_onnx_file}): {onnx_exists}")
                log.info(f"Voice check: Expected JSON file exists ({expected_json_file}): {json_exists}")

                if not (onnx_exists and json_exists):
                    log.warning("Voice check: Expected voice files not found with correct names. May have old files.")
                    should_prompt_download = True
            else:
                log.info(f"Voice check: Expected voice directory does not exist: {expected_voice_dir}")
                should_prompt_download = True

        if should_prompt_download:
            self.__auto_download_attempted = True
            log.info("Voice check: Prompting user to download Welsh voices.")
            # Ask user before downloading
            wx.CallLater(500, self._prompt_voice_download)
        else:
            log.info("Voice check: Valid voices found, skipping auto-download prompt.")

    def _prompt_voice_download(self):
        """Show a dialog asking user if they want to download Welsh voices."""
        message = _(
            "Welsh Neural Voices - First Time Setup\n\n"
            "This addon requires Welsh voice data to function.\n\n"
            "Download details:\n"
            "• Size: Approximately 77 MB\n"
            "• Voice: Welsh multi-speaker neural voice (medium quality, 3 speakers)\n"
            "• Internet connection required\n\n"
            "NVDA will restart automatically after the download completes.\n\n"
            "Would you like to download the Welsh voices now?"
        )

        result = gui.messageBox(
            message,
            # Translators: title of download confirmation dialog
            _("Download Welsh Voices?"),
            wx.YES_NO | wx.ICON_QUESTION
        )

        if result == wx.YES:
            log.info("User confirmed voice download. Starting download.")
            wx.CallAfter(self._auto_download_all_welsh_voices)
        else:
            log.info("User declined voice download.")
            info_message = _(
                "You can download Welsh voices later from:\n"
                "NVDA Menu → Preferences → Settings → Speech → "
                "Select 'Uned Technolegau Iaith - Welsh Neural Voices' as your synthesizer.\n\n"
                "The addon will not function until voices are downloaded."
            )
            gui.messageBox(
                info_message,
                # Translators: title of information dialog
                _("Welsh Voices Not Downloaded"),
                wx.OK | wx.ICON_INFORMATION
            )

    def _auto_download_all_welsh_voices(self):
        """Download all available Welsh voices automatically."""
        def _voice_download_success():
            """Callback when voice download succeeds."""
            pass

        try:
            # Get all available Welsh voices (already filtered by voice_download.py)
            available_voices = voice_download.get_available_voices()

            if not available_voices:
                log.error("No Welsh voices available for download.")
                wx.CallAfter(
                    gui.messageBox,
                    # Translators: error message
                    _(
                        "No Welsh voices are available for download.\n"
                        "Please check your internet connection and try again."
                    ),
                    # Translators: error title
                    _("Error Downloading Welsh Voices"),
                    wx.OK | wx.ICON_ERROR,
                )
                return

            log.info(f"Found {len(available_voices)} Welsh voice(s) to download.")

            # Download each voice
            for voice in available_voices:
                try:
                    log.info(f"Downloading Welsh voice: {voice.key}")
                    downloader = voice_download.PiperVoiceDownloader(voice, _voice_download_success)
                    # Start async download (progress dialog will show, NVDA will restart on completion)
                    downloader.download()
                except Exception as e:
                    log.error(f"Failed to download voice {voice.key}: {e}", exc_info=True)

        except Exception as e:
            log.error("Failed to auto-download Welsh voices", exc_info=True)
            wx.CallAfter(
                gui.messageBox,
                # Translators: error message
                _(
                    "Failed to download Welsh voices automatically.\n"
                    "Error: {error}\n"
                    "Please check NVDA's log for more details."
                ).format(error=str(e)),
                # Translators: error title
                _("Error Downloading Welsh Voices"),
                wx.OK | wx.ICON_ERROR,
            )

    def terminate(self):
        """Cleanup on plugin termination."""
        pass


# Re-export for use by other modules in this package
__all__ = ['TechiaithTextToSpeechSystem', 'TECHIAITH_VOICES_DIR', 'helpers', 'aio']
