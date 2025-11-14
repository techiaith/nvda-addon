@echo off
REM Release automation script for Welsh Neural Voices NVDA Addon (Windows)
REM Usage: scripts\create-release.bat

setlocal enabledelayedexpansion

echo =====================================
echo Welsh Neural Voices NVDA Addon
echo Release Automation Script (Windows)
echo =====================================
echo.

REM Get version from manifest.ini
for /f "tokens=3" %%a in ('findstr /B "version = " addon\manifest.ini') do set VERSION=%%a
set ADDON_FILE=techiaith_tts-%VERSION%.nvda-addon

echo Version: %VERSION%
echo.

REM Check for uncommitted changes
git status --short | findstr /r "^" > nul
if %errorlevel% equ 0 (
    echo Warning: You have uncommitted changes
    git status --short
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo Aborted.
        exit /b 1
    )
)

REM Step 1: Clean previous builds
echo Step 1: Cleaning previous builds...
if exist "%ADDON_FILE%" del /f "%ADDON_FILE%"
if exist "build" rmdir /s /q "build"
echo Done.
echo.

REM Step 2: Build the addon
echo Step 2: Building addon...
where scons >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: scons not found. Please install scons:
    echo   pip install scons
    exit /b 1
)

call scons
if not exist "%ADDON_FILE%" (
    echo Error: Build failed - %ADDON_FILE% not found
    exit /b 1
)
echo Build successful: %ADDON_FILE%
echo.

REM Step 3: Generate SHA256 checksum
echo Step 3: Generating SHA256 checksum...
where certutil >nul 2>&1
if %errorlevel% equ 0 (
    certutil -hashfile "%ADDON_FILE%" SHA256 | findstr /v ":" | findstr /v "SHA256" > "%ADDON_FILE%.sha256"
    set /p CHECKSUM=<"%ADDON_FILE%.sha256"
    set CHECKSUM=!CHECKSUM: =!
    echo !CHECKSUM! > "%ADDON_FILE%.sha256"
    echo SHA256: !CHECKSUM!
    echo Checksum saved to %ADDON_FILE%.sha256
) else (
    echo Warning: certutil not found, skipping checksum generation
)
echo.

REM Step 4: Update RELEASE_NOTES.md with checksum
if defined CHECKSUM (
    echo Step 4: Updating RELEASE_NOTES.md with checksum...
    powershell -Command "(Get-Content RELEASE_NOTES.md) -replace '\(Will be generated during build\)', '%CHECKSUM%' | Set-Content RELEASE_NOTES.md"
    echo RELEASE_NOTES.md updated
    echo.
)

REM Step 5: Commit the checksum update
echo Step 5: Committing changes...
git add RELEASE_NOTES.md addon\manifest.ini buildVars.py
git diff --cached --quiet
if %errorlevel% neq 0 (
    git commit -m "Release v%VERSION%

Update version to %VERSION% and add SHA256 checksum

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    echo Committed changes
) else (
    echo No changes to commit
)
echo.

REM Step 6: Create git tag
echo Step 6: Creating git tag v%VERSION%...
git rev-parse v%VERSION% >nul 2>&1
if %errorlevel% equ 0 (
    echo Warning: Tag v%VERSION% already exists
    set /p RECREATE="Delete and recreate tag? (y/N): "
    if /i "!RECREATE!"=="y" (
        git tag -d v%VERSION%
        git push origin :refs/tags/v%VERSION% 2>nul
        echo Deleted old tag
    ) else (
        echo Aborted.
        exit /b 1
    )
)

git tag -a v%VERSION% -m "Release v%VERSION%

Welsh Neural Voices for NVDA - Beta Release

See RELEASE_NOTES.md for full changelog."
echo Created tag v%VERSION%
echo.

REM Step 7: Push changes and tag
echo Step 7: Pushing to GitHub...
set /p PUSH="Push commits and tags to GitHub? (y/N): "
if /i not "!PUSH!"=="y" (
    echo Aborted. You can manually push later with:
    echo   git push origin main
    echo   git push origin v%VERSION%
    exit /b 1
)

git push origin main
git push origin v%VERSION%
echo Pushed to GitHub
echo.

REM Step 8: Create GitHub release
echo Step 8: Creating GitHub release...
where gh >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo GitHub CLI (gh) not found
    echo.
    echo Manual release instructions:
    echo 1. Go to: https://github.com/techiaith/nvda-addon/releases/new
    echo 2. Select tag: v%VERSION%
    echo 3. Release title: v%VERSION%
    echo 4. Copy release notes from RELEASE_NOTES.md
    echo 5. Upload file: %ADDON_FILE%
    echo 6. Mark as pre-release (beta^)
    echo 7. Publish release
    echo.
    echo Build complete!
    echo Addon file: %ADDON_FILE%
    if defined CHECKSUM echo SHA256: !CHECKSUM!
    exit /b 0
)

echo Creating GitHub release with gh CLI...
gh release create v%VERSION% "%ADDON_FILE%" "%ADDON_FILE%.sha256" --title "v%VERSION%" --notes-file RELEASE_NOTES.md --prerelease

if %errorlevel% equ 0 (
    echo GitHub release created!
) else (
    echo Failed to create release. You can create it manually using the instructions above.
)
echo.

REM Summary
echo =====================================
echo Release Complete!
echo =====================================
echo.
echo Version: %VERSION%
echo Addon file: %ADDON_FILE%
if defined CHECKSUM echo SHA256: !CHECKSUM!
echo Tag: v%VERSION%
echo Release URL: https://github.com/techiaith/nvda-addon/releases/tag/v%VERSION%
echo.
echo Done!

endlocal
