#!/usr/bin/env python3
"""
Flipper Zero File Validator
Verifica la sintassi e struttura dei file .sub, .nfc, .rfid, .ibtn, .ir
Usage: python3 validate-files.py [directory]
"""

import os
import sys
import re
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def ok(msg):
    print(f"  {Colors.GREEN}[OK]{Colors.END} {msg}")


def fail(msg):
    print(f"  {Colors.RED}[FAIL]{Colors.END} {msg}")


def warn(msg):
    print(f"  {Colors.YELLOW}[WARN]{Colors.END} {msg}")


def validate_sub(filepath):
    """Valida file .sub (Sub-GHz)"""
    errors = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    if not lines:
        return ["File vuoto"]

    content = ''.join(lines)

    if 'Filetype: Flipper SubGhz' not in content:
        errors.append("Header 'Filetype: Flipper SubGhz' mancante")

    if 'Version:' not in content:
        errors.append("Campo 'Version' mancante")

    if 'Frequency:' not in content:
        errors.append("Campo 'Frequency' mancante")
    else:
        freq_match = re.search(r'Frequency:\s*(\d+)', content)
        if freq_match:
            freq = int(freq_match.group(1))
            if freq < 300000000 or freq > 928000000:
                if freq < 100000 or freq > 1000000000:
                    errors.append(f"Frequenza fuori range: {freq}")

    if 'Preset:' not in content:
        errors.append("Campo 'Preset' mancante")

    if 'RAW' in content:
        if 'RAW_Data:' not in content:
            errors.append("File RAW senza campo 'RAW_Data'")
    else:
        if 'Protocol:' not in content:
            errors.append("Campo 'Protocol' mancante")

    return errors


def validate_nfc(filepath):
    """Valida file .nfc"""
    errors = []
    with open(filepath, 'r') as f:
        content = f.read()

    if 'Filetype: Flipper NFC device' not in content:
        errors.append("Header 'Filetype: Flipper NFC device' mancante")

    if 'Version:' not in content:
        errors.append("Campo 'Version' mancante")

    if 'UID:' not in content:
        errors.append("Campo 'UID' mancante")

    if 'SAK:' not in content and 'Device type:' not in content:
        errors.append("Campo 'SAK' o 'Device type' mancante")

    return errors


def validate_rfid(filepath):
    """Valida file .rfid"""
    errors = []
    with open(filepath, 'r') as f:
        content = f.read()

    if 'Filetype: Flipper RFID key' not in content:
        errors.append("Header 'Filetype: Flipper RFID key' mancante")

    if 'Key type:' not in content:
        errors.append("Campo 'Key type' mancante")

    if 'Data:' not in content:
        errors.append("Campo 'Data' mancante")

    return errors


def validate_ibtn(filepath):
    """Valida file .ibtn"""
    errors = []
    with open(filepath, 'r') as f:
        content = f.read()

    if 'Filetype: Flipper iButton key' not in content:
        errors.append("Header 'Filetype: Flipper iButton key' mancante")

    if 'Protocol:' not in content:
        errors.append("Campo 'Protocol' mancante")

    return errors


def validate_ir(filepath):
    """Valida file .ir"""
    errors = []
    with open(filepath, 'r') as f:
        content = f.read()

    if 'Filetype: IR signals file' not in content:
        errors.append("Header 'Filetype: IR signals file' mancante")

    names = re.findall(r'^name:\s*(.+)$', content, re.MULTILINE)
    if not names:
        errors.append("Nessun segnale 'name:' trovato")

    types = re.findall(r'^type:\s*(.+)$', content, re.MULTILINE)
    for t in types:
        t = t.strip()
        if t not in ('parsed_signal', 'raw'):
            errors.append(f"Tipo segnale non valido: '{t}'")

    return errors


VALIDATORS = {
    '.sub': validate_sub,
    '.nfc': validate_nfc,
    '.rfid': validate_rfid,
    '.ibtn': validate_ibtn,
    '.ir': validate_ir,
}


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    target_path = Path(target_dir)

    if not target_path.exists():
        print(f"Directory non trovata: {target_dir}")
        sys.exit(1)

    total = 0
    passed = 0
    failed = 0
    warnings = 0

    print(f"\n{'='*60}")
    print(f"Flipper Zero File Validator")
    print(f"Directory: {target_path.resolve()}")
    print(f"{'='*60}\n")

    for ext, validator in VALIDATORS.items():
        files = list(target_path.rglob(f'*{ext}'))
        if not files:
            continue

        print(f"\n--- {ext} files ({len(files)}) ---")

        for filepath in sorted(files):
            total += 1
            rel_path = filepath.relative_to(target_path)

            try:
                errors = validator(filepath)
                if errors:
                    failed += 1
                    fail(str(rel_path))
                    for e in errors:
                        print(f"      -> {e}")
                else:
                    passed += 1
                    ok(str(rel_path))
            except Exception as e:
                failed += 1
                fail(f"{rel_path}: {e}")

    # Check markdown links
    print(f"\n--- Markdown link check ---")
    md_files = list(target_path.rglob('*.md'))
    broken_links = 0

    for md_file in sorted(md_files):
        with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in links:
            if link.startswith(('http://', 'https://', '#', 'mailto:')):
                continue
            link_clean = link.split('#')[0]
            if not link_clean:
                continue
            full_path = (md_file.parent / link_clean).resolve()
            if not full_path.exists():
                if broken_links == 0:
                    warn(f"Link interni rotti trovati:")
                broken_links += 1
                warnings += 1
                print(f"      {md_file.relative_to(target_path)}: '{text}' -> {link_clean}")

    if broken_links == 0:
        ok("Nessun link interno rotto")

    # Summary
    print(f"\n{'='*60}")
    print(f"Risultati: {total} file analizzati")
    print(f"  {Colors.GREEN}Passati: {passed}{Colors.END}")
    print(f"  {Colors.RED}Falliti: {failed}{Colors.END}")
    print(f"  {Colors.YELLOW}Warning: {warnings}{Colors.END}")
    print(f"{'='*60}\n")

    sys.exit(1 if failed > 0 else 0)


if __name__ == '__main__':
    main()
