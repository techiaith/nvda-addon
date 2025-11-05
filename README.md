# Uned Technolegau Iaith - Welsh Neural Voices for NVDA

> **⚠️ BETA SOFTWARE** - Version 2025.11.0
> This is beta software currently in testing. Please report any issues on the [GitHub issues page](https://github.com/techiaith/nvda-addon/issues).

**Welsh-only neural text-to-speech for NVDA. Only Welsh (Cymraeg) voices are supported.**

This add-on implements a speech synthesizer driver for NVDA using neural TTS models. It supports [Piper](https://github.com/rhasspy/piper) Welsh voices.

[Piper](https://github.com/rhasspy/piper) is a fast, local neural text to speech system that sounds great and is optimized for low-end devices such as the Raspberry Pi.

You can listen to Piper's voice samples here: [Piper voice samples](https://rhasspy.github.io/piper-samples/).

This add-on uses [Sonata: A cross-platform Rust engine for neural TTS models](https://github.com/mush42/sonata) which is being developed by Musharraf Omer.

## System Requirements

- **Operating System:** Windows 10/11 (x86 or x64 architecture)
  - ⚠️ **ARM64 Windows is NOT supported** - The addon will not work on ARM-based Windows devices (e.g., Surface Pro X, ARM laptops)
- **NVDA Version:** 2025.1 or later
- **Internet Connection:** Required for initial voice download (approximately 77 MB)

## What's Included

- **Version:** 2025.11.0 Beta
- **Welsh Voice:** Multi-speaker neural voice (medium quality, 3 speakers)
- **Language Support:** Welsh (Cymraeg) only
- **Auto-download:** Voice is downloaded automatically on first run


# Installation

## Downloading the add-on

You can find the add-on package under the assets section of the [release page](https://github.com/techiaith/nvda-addon/releases/latest)

## Automatic Voice Installation

**Welsh voices are downloaded on first run with your permission.**

When you install this add-on for the first time:

1. Install the add-on and restart NVDA
2. A dialog will appear asking if you want to download Welsh voices (approximately 77 MB)
3. If you click "Yes", the download will begin and show progress updates
4. NVDA will announce progress at 25%, 50%, and 75% completion
5. When complete, a confirmation dialog will appear
6. Click "OK" to restart NVDA and activate the Welsh voices

If you click "No" on the initial dialog, you can download voices later through NVDA's speech settings.

## Switching Between Voices

To switch between different Welsh voices or adjust voice settings:

1. Open NVDA Settings (NVDA+N, then P for Preferences, then S for Settings)
2. Go to the Speech category
3. Select "Uned Technolegau Iaith - Welsh Neural Voices" as your synthesizer
4. Use the Voice dropdown to choose between the installed Welsh voices
5. Adjust rate, pitch, and volume as desired

All voice management is done through NVDA's standard synthesizer settings.

## A note on voice quality

The currently available voices are trained using freely available TTS datasets, which are generally of low quality (mostly public domain audio books or research quality recordings).

Additionally, these datasets are not comprehensive, hence some voices may exhibit incorrect or weird pronunciation. Both issues could be resolved by using better datasets for training.

Luckily, the `Piper` developer and some developers from the blind and vision-impaired community are working on training better voices.

## Known Limitations (Beta)

- **Platform:** Only works on x86/x64 Windows. ARM64 Windows is not supported.
- **Voice Selection:** Currently only includes one Welsh voice with 3 speaker variants (medium quality).
- **Testing Status:** This is beta software - limited testing has been performed.
- **NVDA Compatibility:** Requires NVDA 2025.1 or later.
- **First Run:** Requires internet connection for automatic voice download on first use.

If you encounter issues, please report them on the [GitHub issues page](https://github.com/techiaith/nvda-addon/issues).

# Development

## Build Requirements

You need the following software to build this NVDA add-on:

* Python 3.7 or later - [Python Website](https://www.python.org)
* SCons 4.3.0 or later - Install via: `pip install scons`
* GNU Gettext tools - For localization support
* Markdown 3.3.0 or later - Install via: `pip install markdown`

## Build Instructions

```bash
# Build the addon
scons

# Generate translation template
scons pot
```

The built addon file will be: `techiaith_tts-{version}.nvda-addon`

# Acknowledgments

This addon is based on [Sonata-NVDA](https://github.com/mush42/sonata-nvda) by Musharraf Omer, which has been modified to work exclusively with Welsh (Cymraeg) voices.

We gratefully acknowledge:
- **Musharraf Omer** for developing [Sonata](https://github.com/mush42/sonata) - the cross-platform Rust engine for neural TTS models that powers this addon
- **Musharraf Omer** for the original [Sonata-NVDA addon](https://github.com/mush42/sonata-nvda) which this work is based upon
- The **Piper TTS project** and **Rhasspy community** for developing high-quality neural TTS voices

# License

Copyright(c) 2024-2025, Stephen Russell, Uned Technolegau Iaith / Language Technologies Unit, Bangor University.

This software is licensed under The GNU GENERAL PUBLIC LICENSE Version 2 (GPL v2).

Based on Sonata-NVDA by Musharraf Omer, also licensed under GPL v2.
