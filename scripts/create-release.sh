#!/bin/bash
# Release automation script for Welsh Neural Voices NVDA Addon
# Usage: ./scripts/create-release.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get version from manifest.ini
VERSION=$(grep "^version = " addon/manifest.ini | cut -d' ' -f3)
ADDON_FILE="techiaith_tts-${VERSION}.nvda-addon"

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}Welsh Neural Voices NVDA Addon${NC}"
echo -e "${BLUE}Release Automation Script${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""
echo -e "${GREEN}Version: ${VERSION}${NC}"
echo ""

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}Warning: You are on branch '${CURRENT_BRANCH}', not 'main'${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: You have uncommitted changes${NC}"
    git status --short
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
fi

# Step 1: Clean previous builds
echo -e "${BLUE}Step 1: Cleaning previous builds...${NC}"
if [ -f "$ADDON_FILE" ]; then
    rm "$ADDON_FILE"
    echo -e "${GREEN}Removed old addon file${NC}"
fi
if [ -d "build" ]; then
    rm -rf build
    echo -e "${GREEN}Removed build directory${NC}"
fi

# Step 2: Build the addon
echo ""
echo -e "${BLUE}Step 2: Building addon...${NC}"
if ! command -v scons &> /dev/null; then
    echo -e "${RED}Error: scons not found. Please install scons:${NC}"
    echo "  pip install scons"
    exit 1
fi

scons

if [ ! -f "$ADDON_FILE" ]; then
    echo -e "${RED}Error: Build failed - $ADDON_FILE not found${NC}"
    exit 1
fi
echo -e "${GREEN}Build successful: $ADDON_FILE${NC}"

# Step 3: Generate SHA256 checksum
echo ""
echo -e "${BLUE}Step 3: Generating SHA256 checksum...${NC}"
if command -v sha256sum &> /dev/null; then
    CHECKSUM=$(sha256sum "$ADDON_FILE" | cut -d' ' -f1)
elif command -v shasum &> /dev/null; then
    CHECKSUM=$(shasum -a 256 "$ADDON_FILE" | cut -d' ' -f1)
else
    echo -e "${RED}Error: Neither sha256sum nor shasum found${NC}"
    exit 1
fi
echo -e "${GREEN}SHA256: $CHECKSUM${NC}"

# Save checksum to file
echo "$CHECKSUM" > "${ADDON_FILE}.sha256"
echo -e "${GREEN}Checksum saved to ${ADDON_FILE}.sha256${NC}"

# Step 4: Update RELEASE_NOTES.md with checksum
echo ""
echo -e "${BLUE}Step 4: Updating RELEASE_NOTES.md with checksum...${NC}"
sed -i "s/(Will be generated during build)/$CHECKSUM/" RELEASE_NOTES.md
echo -e "${GREEN}RELEASE_NOTES.md updated${NC}"

# Step 5: Commit the checksum update
echo ""
echo -e "${BLUE}Step 5: Committing checksum update...${NC}"
git add RELEASE_NOTES.md
if git diff --cached --quiet; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    git commit -m "Update SHA256 checksum for v${VERSION}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    echo -e "${GREEN}Committed checksum update${NC}"
fi

# Step 6: Create git tag
echo ""
echo -e "${BLUE}Step 6: Creating git tag v${VERSION}...${NC}"
if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: Tag v${VERSION} already exists${NC}"
    read -p "Delete and recreate tag? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "v${VERSION}"
        git push origin ":refs/tags/v${VERSION}" 2>/dev/null || true
        echo -e "${GREEN}Deleted old tag${NC}"
    else
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
fi

git tag -a "v${VERSION}" -m "Release v${VERSION}

Welsh Neural Voices for NVDA - Beta Release

See RELEASE_NOTES.md for full changelog."

echo -e "${GREEN}Created tag v${VERSION}${NC}"

# Step 7: Push changes and tag
echo ""
echo -e "${BLUE}Step 7: Pushing to GitHub...${NC}"
echo -e "${YELLOW}This will push commits and tags to GitHub${NC}"
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Aborted. You can manually push later with:${NC}"
    echo "  git push origin main"
    echo "  git push origin v${VERSION}"
    exit 1
fi

git push origin main
git push origin "v${VERSION}"
echo -e "${GREEN}Pushed to GitHub${NC}"

# Step 8: Create GitHub release
echo ""
echo -e "${BLUE}Step 8: Creating GitHub release...${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI (gh) not found${NC}"
    echo ""
    echo -e "${BLUE}Manual release instructions:${NC}"
    echo "1. Go to: https://github.com/techiaith/nvda-addon/releases/new"
    echo "2. Select tag: v${VERSION}"
    echo "3. Release title: v${VERSION}"
    echo "4. Copy release notes from RELEASE_NOTES.md"
    echo "5. Upload file: ${ADDON_FILE}"
    echo "6. Mark as pre-release (beta)"
    echo "7. Publish release"
    echo ""
    echo -e "${GREEN}Build complete!${NC}"
    echo -e "Addon file: ${BLUE}${ADDON_FILE}${NC}"
    echo -e "SHA256: ${BLUE}${CHECKSUM}${NC}"
    exit 0
fi

# Extract release notes for this version
RELEASE_NOTES=$(awk '/^## What'\''s New in v'${VERSION}'/,/^## Previous Release/' RELEASE_NOTES.md | head -n -1)

echo -e "${YELLOW}Creating GitHub release with gh CLI...${NC}"
gh release create "v${VERSION}" \
    "$ADDON_FILE" \
    "${ADDON_FILE}.sha256" \
    --title "v${VERSION}" \
    --notes "$RELEASE_NOTES" \
    --prerelease

echo -e "${GREEN}GitHub release created!${NC}"

# Summary
echo ""
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}Release Complete!${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""
echo -e "Version: ${GREEN}${VERSION}${NC}"
echo -e "Addon file: ${BLUE}${ADDON_FILE}${NC}"
echo -e "SHA256: ${BLUE}${CHECKSUM}${NC}"
echo -e "Tag: ${BLUE}v${VERSION}${NC}"
echo -e "Release URL: ${BLUE}https://github.com/techiaith/nvda-addon/releases/tag/v${VERSION}${NC}"
echo ""
echo -e "${GREEN}Done!${NC}"
