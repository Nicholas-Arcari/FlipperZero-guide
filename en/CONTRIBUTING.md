# Contributing - Contribution Guide

Thank you for your interest in contributing to this project. This guide describes how to participate effectively.

---

## How to Contribute

### Reporting Errors or Issues
1. Open an **Issue** on GitHub
2. Describe the problem with sufficient detail (file, section, what is wrong)
3. If possible, suggest the correction

### Adding Content
1. **Fork** the repository
2. Create a **branch** with a descriptive name (`add-subghz-scenario-parking`, `fix-nfc-typo`)
3. Make your changes following the guidelines below
4. Open a **Pull Request** with a description of what you changed and why

---

## Style Guidelines

### Language
- **Italian** for all main content
- Technical terms in English where no established Italian equivalent exists (e.g., "replay attack", not "attacco di riproduzione")
- Accents with apostrophe (`e'`, `piu'`, `perche'`) for compatibility with all editors

### File Structure
Each main module follows the 8-file structure:

```
Module/
├── README.md                    ← Short index (~100-150 lines)
├── 01-Fondamenti-Tecnici.md     ← How the protocol works
├── 02-Hardware-e-Limiti.md      ← Specifications and real-world limits
├── 03-Protocolli.md             ← Protocol deep dive
├── 04-Guida-Operativa.md        ← Step-by-step for each tool
├── 05-Scenari-Reali.md          ← Real-world pentest scenarios
├── 06-Attacchi-e-Difese.md      ← Attack vectors + countermeasures
├── 07-Aspetti-Legali.md         ← IT/EU regulations
└── 08-Esperienza-Personale.md   ← Field notes, troubleshooting
```

### Formatting
- Markdown tables for structured data
- Code blocks with specified language where applicable
- `> Nota personale:` for direct experiences (blockquote)
- Avoid single headings (not an H2 with just one line below)
- Cross-reference to other modules where useful

### Real-World Scenarios
Each scenario must include:
1. **Context** -- type of engagement, environment
2. **Objective** -- what you want to test
3. **Procedure** -- detailed step-by-step
4. **Result/Finding** -- what was found
5. **Impact** -- CVSS or qualitative classification
6. **Remediation** -- recommendation for the client

### BadUSB Payloads
Payloads must:
- Have a header with: description, target OS, prerequisites, keyboard layout
- Be commented with `REM` for each logical block
- Include realistic `DELAY` values
- Specify if elevated privileges are required
- NOT contain hardcoded attacker IP/URLs (use placeholder `ATTACKER_IP`)

---

## What NOT to Do

- Do not add binary files (firmware, executables) -- only link to official releases
- Do not include real data from other people's devices (UIDs, keys, credentials)
- Do not remove existing content without discussion in an Issue
- Do not add content in English (unless it is code or commands)
- Do not add watermarks, logos, or personal branding

---

## Areas Where Contributions Are Needed

- New real-world pentest scenarios (with anonymized context)
- Tested BadUSB payloads for different OSes and configurations
- Technical corrections (protocols, specifications, commands)
- Translations (when/if the English section is opened)
- Improvements to Mermaid diagrams
- New glossary entries

---

## License

By contributing, you agree that your work will be distributed under the same license as the repository ([MIT License](LICENSE)).
