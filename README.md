# nvda-addon

## Getting started

To use the add on simply download the *uti_cy-0.1.nvda-addon* file and follw the instructions here.

## Build process

## Requirements

You need the following software to use this code for your NVDA add-on development and packaging:

* a Python distribution (3.7 or later is recommended). Check the [Python Website](https://www.python.org) for Windows Installers.
* Scons - [Website](https://www.scons.org/) - version 4.3.0 or later. You can install it via PIP.
* GNU Gettext tools, if you want to have localization support for your add-on - Recommended. Any Linux distro or cygwin have those installed. You can find windows builds [here](https://gnuwin32.sourceforge.net/downlinks/gettext.php).
* Markdown 3.3.0 or later, if you want to convert documentation files to HTML documents. You can install it via PIP.

Note, that you may not need these tools in a local build environment, if you are using [Appveyor](https://appveyor.com/) or [GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions), to build and package your add-ons.

## Build instructions

`C:\Path\To\Addon\Dir> scons`
