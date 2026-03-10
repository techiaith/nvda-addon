# Welsh Neural Voices for NVDA - v2026.3.9 Beta

> **⚠️ BETA SOFTWARE** - This is a beta release for testing. Please report issues on our [GitHub issues page](https://github.com/techiaith/nvda-addon/issues).

## About This Release

Welsh-only neural text-to-speech for NVDA using Piper models. This addon provides high-quality Welsh (Cymraeg) voices for NVDA screen reader users.

## What's New in v2026.3.9

### Improvements
- **Decoupled voice metadata from addon** — downloads now fetch file sizes and SHA256 hashes from HuggingFace API
- **Switched hash verification from MD5 to SHA256** for improved security
- **Graceful fallback when API is unreachable** — skips hash verification instead of failing
- **Model files on HuggingFace can now be updated without redeploying the addon**

### Build Metadata Fixes
- Fixed NVDA version fields (were floats, now strings) — prevents JSON generation errors
- Added license URL to addon metadata
- Version bump to 2026.3.9

## What's New in v2025.11.2

### Bug Fixes
- **Fixed auto-download popup not appearing**: The popup that prompts users to download voices on first run now correctly appears when no valid voice files are found
- **Updated voice repository**: Changed voice file repository from `cy_GB-bu_tts` to `cy_en_GB-bu_tts` to reflect the new repository structure
- **Added voice file validation**: The addon now verifies that the correct voice files exist, not just the directory
- **Enhanced diagnostic logging**: Added detailed logging (prefixed with "Voice check:") to help troubleshoot voice detection issues

### Technical Changes
- Voice files now use `cy_en_GB-bu_tts` naming convention
- Download URL updated to point to `techiaith/cy_en_GB-bu_tts` repository
- Voice check now validates actual ONNX and JSON file names

## Previous Release (v2025.11.1)

### Bug Fixes
- Minor bug fixes and stability improvements

## Previous Release (v2025.11.0)

### Features
- **Welsh Neural Voice:** Multi-speaker neural voice (3 speakers, medium quality)
- **Automatic Download:** First-run setup with user confirmation
- **Bilingual:** Full Welsh and English documentation
- **Accessible:** Progress announcements and clear user feedback

### Accessibility Improvements
- User confirmation dialog before downloading (77 MB)
- Progress announcements at 25%, 50%, and 75% completion
- Completion dialog before NVDA restart
- No surprise restarts - user has control

### Installation

1. Download `techiaith_tts-2026.3.9.nvda-addon` from the assets below
2. Open with NVDA (or use NVDA menu → Tools → Manage add-ons → Install)
3. Restart NVDA when prompted
4. A dialog will ask if you want to download Welsh voices (77 MB)
5. Click Yes to download, then OK when complete to restart

## System Requirements

- **Operating System:** Windows 10/11 (x86 or x64 only)
  - ⚠️ **ARM64 Windows NOT supported**
- **NVDA Version:** 2025.1 or later
- **Internet Connection:** Required for initial voice download (~77 MB)

## Known Limitations (Beta)

- Only one Welsh voice included (3 speaker variants)
- x86/x64 Windows only - ARM64 not supported
- NVDA 2025.1 or later required
- Beta software - limited testing performed

## Technical Details

- **Version:** 2026.3.9 (year.month.day format)
- **Author:** Stephen Russell, Uned Technolegau Iaith / Language Technologies Unit, Bangor University
- **Based on:** [Sonata-NVDA](https://github.com/mush42/sonata-nvda) by Musharraf Omer
- **License:** GPL v2
- **Voice Engine:** [Piper TTS](https://github.com/rhasspy/piper)
- **Runtime:** [Sonata](https://github.com/mush42/sonata) by Musharraf Omer

## Acknowledgments

- **Musharraf Omer** - for Sonata and Sonata-NVDA
- **Piper TTS project** and **Rhasspy community** - for neural voice models

## Support

- **Issues:** https://github.com/techiaith/nvda-addon/issues
- **Website:** https://techiaith.cymru/cynnyrch/nvda/

## SHA256 Checksum

```
UPDATE_AFTER_BUILD
```
