# coding: utf-8

# Copyright (c) 2023 Musharraf Omer
# This file is covered by the GNU General Public License.


import math
import os
import shutil
import tempfile
import typing
from dataclasses import dataclass
from enum import Enum
from functools import partial
from hashlib import md5
from urllib.parse import urlparse

import wx
import core
import gui
from logHandler import log

from . import TechiaithTextToSpeechSystem, helpers, TECHIAITH_VOICES_DIR

with helpers.import_bundled_library():
    import mureq as request
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path


VOICE_DOWNLOAD_URL_PREFIX = "https://huggingface.co/techiaith/cy_GB-bu_tts/resolve/main"
THREAD_POOL_EXECUTOR = ThreadPoolExecutor()


class VoiceQualityLevel(Enum):
    XLow = "x_low"
    Low = "low"
    Medium = "medium"
    High = "high"

    def __str__(self):
        return " ".join(v.title() for v in self.value.split("_"))


@dataclass
class VoiceFile:
    file_path: str
    size_in_bytes: int
    md5hash: str

    def __post_init__(self):
        self.name = os.path.split(self.file_path)[-1]
        self.download_url = f"{VOICE_DOWNLOAD_URL_PREFIX}/{self.file_path}"


@dataclass(eq=False)
class VoiceLanguage:
    code: str
    family: str
    name_native: str
    name_english: str

    def __str__(self):
        return self.code.replace("_", "-")

    def __eq__(self, other):
        if isinstance(other, VoiceLanguage):
            return self.code == other.code
        return NotImplemented

    def __hash__(self):
        return hash(self.code)


@dataclass
class PiperVoice:
    key: str
    name: str
    quality: VoiceQualityLevel
    language: VoiceLanguage
    files: typing.List[VoiceFile]

    @classmethod
    def from_list_of_dicts(cls, voice_data):
        retval = []
        for data in voice_data:
            file_list = []
            for (path, finfo) in data["files"].items():
                file_list.append(VoiceFile(
                    file_path=path,
                    size_in_bytes=finfo["size_bytes"],
                    md5hash=finfo["md5_digest"]
                ))
            lang_info = data["language"]
            language = VoiceLanguage(
                code=lang_info["code"],
                family=lang_info["family"],
                name_native=lang_info["name_native"],
                name_english=lang_info["name_english"],
            )
            retval.append(cls(
                key=data["key"],
                name=data["name"],
                quality=VoiceQualityLevel(data["quality"]),
                language=language,
                files=file_list,
            ))
        return retval


class PiperVoiceDownloader:
    def __init__(self, voice: PiperVoice, success_callback):
        self.voice = voice
        self.success_callback = success_callback
        self.temp_download_dir = tempfile.TemporaryDirectory()
        self.progress_dialog = None

    def update_progress(self, progress):
        message = _("Downloaded: {progress}%").format(progress=progress)
        self.progress_dialog.Update(progress, message)
        # Announce progress for screen readers at key milestones
        if progress in (25, 50, 75):
            import ui
            ui.message(message)

    def done_callback(self, result):
        has_error = isinstance(result, Exception)
        if not has_error:
            self.progress_dialog.Update(
                0,
                # Translators: message shown in the voice download progress dialog
                _("Installing voice")
            )
            hashes = {
                file.md5hash: md5hash
                for (file, __, md5hash) in result
                if file.md5hash  # Only check hash if it's provided (not empty)
            }
            if hashes and not all(k == v for (k, v) in hashes.items()):
                has_error = True
                log.error("File hashes do not match")
            else:
                voice_dir = Path(TECHIAITH_VOICES_DIR).joinpath(self.voice.key)
                voice_dir.mkdir(parents=True, exist_ok=True)
                for file, src,  __ in result:
                    dst = os.path.join(voice_dir, file.name)
                    try:
                        shutil.copy(src, dst)
                    except IOError:
                        log.exception("Failed to copy file: {file}", exc_info=True)
                        has_error = True

        self.progress_dialog.Hide()
        self.progress_dialog.Destroy()
        del self.progress_dialog

        if not has_error:
            self.success_callback()
            # Show completion dialog before restarting NVDA
            wx.CallAfter(self._show_completion_and_restart)
        else:
            wx.CallAfter(
                gui.messageBox,
                _(
                    "Cannot download voice {voice}.\nPlease check your connection and try again."
                ).format(voice=self.voice.key),
                _("Download failed"),
                style=wx.ICON_ERROR,
            )
            log.exception(
                f"Failed to download voice.\nException: {result}"
            )

    def _show_completion_and_restart(self):
        """Show completion dialog and restart NVDA after user acknowledges."""
        result = gui.messageBox(
            # Translators: message shown when voice download completes successfully
            _(
                "Welsh voices have been downloaded successfully!\n\n"
                "NVDA needs to restart to load the new voices.\n\n"
                "Click OK to restart NVDA now."
            ),
            # Translators: title of download completion dialog
            _("Download Complete"),
            wx.OK | wx.ICON_INFORMATION
        )
        # Restart after user acknowledges
        core.restart()

    def download(self):
        self.progress_dialog = wx.ProgressDialog(
            # Translators: title of a progress dialog
            title=_("Downloading voice {voice}").format(
                voice=self.voice.key
            ),
            # Translators: message of a progress dialog
            message=_("Retrieving download information..."),
            parent=gui.mainFrame,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
        )
        self.progress_dialog.CenterOnScreen()
        THREAD_POOL_EXECUTOR.submit(self.download_voice_files).add_done_callback(partial(self._done_callback_wrapper, self.done_callback))

    def download_voice_files(self):
        retvals = []
        for file in self.voice.files:
            self.progress_dialog.Update(
                0,
                # Translators: message shown in progress dialog
                _("Downloading file: {file}").format(file=file.name)
            )
            result = self._do_download_file(file, self.temp_download_dir.name, self.update_progress)
            retvals.append(result)

        return retvals

    @classmethod
    def _do_download_file(cls, file, download_dir, progress_callback):
        target_file = os.path.join(download_dir, file.name)
        hasher = md5()
        total_size = file.size_in_bytes
        downloaded_til_now = 0
        with request.yield_response('GET', file.download_url) as response:
            # Handle all HTTP redirect status codes
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location")
                # Convert relative redirect URLs to absolute URLs
                if location.startswith("/"):
                    # Relative URL - extract base from original URL
                    parsed = urlparse(file.download_url)
                    file.download_url = f"{parsed.scheme}://{parsed.netloc}{location}"
                else:
                    # Already absolute
                    file.download_url = location
                return cls._do_download_file(file, download_dir, progress_callback)
            with open(target_file, "wb") as file_buffer:
                while True:
                    chunk = response.read(4096)
                    if not chunk:
                        break
                    file_buffer.write(chunk)
                    hasher.update(chunk)
                    downloaded_til_now += len(chunk)
                    progress = math.floor((downloaded_til_now / total_size) * 100)
                    progress_callback(progress)

        return (file, target_file, hasher.hexdigest())

    @staticmethod
    def _done_callback_wrapper(done_callback, future):
        if done_callback is None:
            return
        try:
            result = future.result()
        except Exception as e:
            done_callback(e)
        else:
            done_callback(result)


def get_available_voices():
    """Get available Welsh voices for download.

    Returns a hardcoded list containing the Welsh multi-speaker voice if it's not installed.
    """
    # Check if voice is already installed
    installed_voices = TechiaithTextToSpeechSystem.load_piper_voices_from_nvda_config_dir()
    installed_voice_keys = {voice.key for voice in installed_voices}

    # Hardcoded Welsh voice details
    voice_key = "cy-ms-medium"

    # If already installed, return empty list
    if voice_key in installed_voice_keys:
        return []

    # Create voice data structure
    voice_data = {
        "key": voice_key,
        "name": "ms",
        "quality": "medium",
        "language": {
            "code": "cy",
            "family": "cy",
            "name_native": "Cymraeg",
            "name_english": "Welsh",
        },
        "files": {
            "ms_cy_en.onnx": {
                "size_bytes": 77061326,
                "md5_digest": "aee1f60f7329b1e67047ad18446e646d"
            },
            "ms_cy_en.onnx.json": {
                "size_bytes": 7182,
                "md5_digest": "da34be5e46d815dea63eafecaa426dc6"
            }
        }
    }

    # Convert to PiperVoice object
    return PiperVoice.from_list_of_dicts([voice_data])
