# Release Automation Scripts

This directory contains scripts to automate the release process for the Welsh Neural Voices NVDA addon.

## Scripts

### `create-release.sh` (Linux/macOS)

Bash script for Unix-based systems.

**Usage:**
```bash
./scripts/create-release.sh
```

### `create-release.bat` (Windows)

Batch script for Windows systems.

**Usage:**
```cmd
scripts\create-release.bat
```

## What the Scripts Do

Both scripts automate the following steps:

1. **Clean previous builds** - Remove old build artifacts
2. **Build the addon** - Run `scons` to build the `.nvda-addon` file
3. **Generate SHA256 checksum** - Calculate checksum for the built file
4. **Update release notes** - Insert the checksum into `RELEASE_NOTES.md`
5. **Commit changes** - Commit the checksum update to git
6. **Create git tag** - Tag the release with version number (e.g., `v2025.11.2`)
7. **Push to GitHub** - Push commits and tags to the remote repository
8. **Create GitHub release** - Use GitHub CLI to create the release (if available)

## Prerequisites

### Required
- **Git** - For version control operations
- **SCons** - For building the addon (`pip install scons`)
- **Python 3** - For running SCons

### Optional (for automated GitHub release)
- **GitHub CLI** (`gh`) - For creating GitHub releases automatically
  - Install: https://cli.github.com/
  - Authenticate: `gh auth login`

### Platform-Specific Requirements

**Linux/macOS:**
- Bash shell
- `sha256sum` or `shasum` command (usually pre-installed)

**Windows:**
- Command Prompt or PowerShell
- `certutil` command (usually pre-installed)

## Manual Release (if GitHub CLI not available)

If you don't have GitHub CLI installed, the scripts will provide instructions for creating the release manually:

1. Go to: https://github.com/techiaith/nvda-addon/releases/new
2. Select the tag created by the script (e.g., `v2025.11.2`)
3. Set release title to the version (e.g., `v2025.11.2`)
4. Copy release notes from `RELEASE_NOTES.md`
5. Upload the built `.nvda-addon` file
6. Mark as pre-release (beta)
7. Publish release

## Version Management

Version numbers are read from `addon/manifest.ini`. To create a new release:

1. Update version in:
   - `addon/manifest.ini`
   - `buildVars.py`
   - `RELEASE_NOTES.md` (add new section)

2. Run the release script:
   ```bash
   ./scripts/create-release.sh  # Linux/macOS
   # or
   scripts\create-release.bat   # Windows
   ```

## Troubleshooting

### "scons: command not found"
Install SCons:
```bash
pip install scons
```

### "gh: command not found"
Install GitHub CLI or create the release manually (see instructions above).

### Tag already exists
The script will ask if you want to delete and recreate the tag. This is useful for fixing mistakes.

### Uncommitted changes
The script will warn you if there are uncommitted changes and ask if you want to continue.

## Notes

- The scripts automatically mark releases as "pre-release" since this is beta software
- SHA256 checksums are included for security verification
- All git commits include proper attribution to Claude Code
- The scripts use color output for better readability (Linux/macOS only)
