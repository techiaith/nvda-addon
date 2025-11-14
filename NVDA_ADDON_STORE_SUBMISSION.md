# NVDA Addon Store Submission Guide

## Step-by-Step Instructions for Submitting to NVDA Addon Store

### Prerequisites
✅ GitHub release must be published first
✅ Addon file must be publicly accessible at the download URL

---

## Submission Form Values

Use these exact values when filling out the NVDA addon store submission form:

### 1. Go to Submission Page
**URL:** https://github.com/nvaccess/addon-datastore/issues/new/choose

**Click:** "Get started" button next to "Add-on registration"

---

### 2. Fill Out the Form

Copy and paste these values into the form:

#### Basic Information

**Add-on ID:**
```
techiaith_tts
```

**Display Name:**
```
Uned Technolegau Iaith - Welsh Neural Voices
```

**Publisher:**
```
Uned Technolegau Iaith / Language Technologies Unit
```

---

#### Download Information

**Download URL:**
```
https://github.com/techiaith/nvda-addon/releases/download/v2025.11.1/techiaith_tts-2025.11.1.nvda-addon
```

**SHA256 Checksum:**
```
4ed6dc65ae4f41045169b6b7fabf5d80e95d3f8cfc1b0734aac099812b1e6f8b
```

---

#### Version Information

**Version:**
```
2025.11.1
```

**Channel:**
```
beta
```

**Minimum NVDA Version:**
```
2025.1.0
```

**Last Tested NVDA Version:**
```
2025.3.0
```

---

#### URLs

**Homepage:**
```
https://techiaith.cymru/cynnyrch/nvda/
```

**Source Code URL:**
```
https://github.com/techiaith/nvda-addon
```

**License URL:**
```
https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
```

---

#### Description

**Description:**
```
Automatic Welsh (Cymraeg) neural text-to-speech for NVDA using Piper models. All Welsh voices are downloaded automatically on first run.
```

**License:**
```
GPL 2
```

---

### 3. Submit and Wait

1. **Click** "Submit new issue"
2. The system will automatically:
   - Create a GitHub issue
   - Create a pull request
   - Run validation checks
   - Scan for security issues

3. **Wait for checks to complete** (usually 5-10 minutes)
   - ✅ Download URL validation
   - ✅ SHA256 checksum verification
   - ✅ NVDA version compatibility
   - ✅ Metadata validation
   - ✅ Security scans (CodeQL, VirusTotal)

4. **First-time submission:**
   - NV Access staff will manually review
   - May take a few days
   - They'll comment on the issue if changes needed

5. **After approval:**
   - PR will merge automatically
   - Addon appears in NVDA addon store within hours

---

## Important Notes

⚠️ **First Submission:** Your first submission requires manual approval from NV Access staff. Be patient!

⚠️ **Immutable Versions:** Once published, you cannot change version 2025.11.1. Any fixes require a new version (e.g., 2025.11.2).

⚠️ **Beta Channel:** Users must opt-in to see beta releases in the addon store.

✅ **No Manual Review:** NV Access does not manually review your code before acceptance. Security scans are automated.

---

## After Submission

### Monitor Your Submission

1. **Check the issue:** Watch for comments from automation or NV Access staff
2. **Check the PR:** Look for validation results
3. **Fix any issues:** If validation fails, you may need to update and resubmit

### When Approved

1. Your addon will appear in the NVDA addon store
2. Users can install from: NVDA → Tools → Manage Add-ons → Available Add-ons
3. Update announcements can be posted on the GitHub releases page

---

## Troubleshooting

### Common Validation Errors

**Download URL not accessible:**
- Ensure GitHub release is published (not draft)
- Check URL is exactly correct

**SHA256 mismatch:**
- Recalculate: `sha256sum techiaith_tts-2025.11.1.nvda-addon`
- Ensure you're checking the file FROM the GitHub release

**Invalid NVDA version:**
- Must be actual NVDA API versions
- Format: YYYY.M.P (e.g., 2025.1.0, 2025.3.0)

**Metadata mismatch:**
- Display name must match manifest summary
- Description must match manifest description

---

## Support

If you have questions during submission:
- **NVDA Addon Store:** https://github.com/nvaccess/addon-datastore
- **Documentation:** https://github.com/nvaccess/addon-datastore/blob/master/docs/submitters/submissionGuide.md
