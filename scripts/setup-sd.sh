#!/bin/bash
# =============================================================================
# Flipper Zero SD Card Setup Script
# Prepara la microSD con la struttura corretta e scarica i database necessari
# Usage: ./setup-sd.sh /path/to/sd/mount
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SD_PATH="${1:-}"

if [ -z "$SD_PATH" ]; then
    echo -e "${RED}[!] Usage: $0 /path/to/flipper/sd${NC}"
    echo "    Esempio: $0 /media/$USER/Flipper"
    exit 1
fi

if [ ! -d "$SD_PATH" ]; then
    echo -e "${RED}[!] Directory non trovata: $SD_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Flipper Zero SD Card Setup${NC}"
echo -e "[*] Target: $SD_PATH"
echo ""

# --- Struttura directory ---
echo -e "${YELLOW}[1/5] Creazione struttura directory...${NC}"

DIRS=(
    "subghz"
    "subghz/assets"
    "nfc"
    "nfc/assets"
    "lfrfid"
    "ibutton"
    "infrared"
    "infrared/assets"
    "badusb"
    "apps"
    "apps_data"
    "update"
    "music_player"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$SD_PATH/$dir"
    echo "  [+] $dir/"
done

# --- Download database IR ---
echo ""
echo -e "${YELLOW}[2/5] Download database IR universale...${NC}"

if command -v git &> /dev/null; then
    if [ ! -d "/tmp/flipper-irdb" ]; then
        git clone --depth 1 https://github.com/Lucaslhm/Flipper-IRDB.git /tmp/flipper-irdb 2>/dev/null || {
            echo -e "${RED}  [!] Download IRDB fallito, continuo...${NC}"
        }
    fi
    if [ -d "/tmp/flipper-irdb" ]; then
        cp -r /tmp/flipper-irdb/* "$SD_PATH/infrared/" 2>/dev/null || true
        echo -e "${GREEN}  [+] Database IR copiato${NC}"
    fi
else
    echo -e "${YELLOW}  [!] git non trovato, skip download IRDB${NC}"
fi

# --- Download dizionari NFC ---
echo ""
echo -e "${YELLOW}[3/5] Download dizionari chiavi MIFARE...${NC}"

MIFARE_DICT_URL="https://raw.githubusercontent.com/RfidResearchGroup/proxmark3/master/client/dictionaries/mfc_default_keys.dic"
if command -v curl &> /dev/null; then
    curl -sL "$MIFARE_DICT_URL" -o "$SD_PATH/nfc/assets/mf_classic_dict_user.nfc" 2>/dev/null && \
        echo -e "${GREEN}  [+] Dizionario MIFARE scaricato${NC}" || \
        echo -e "${YELLOW}  [!] Download dizionario fallito, continuo...${NC}"
elif command -v wget &> /dev/null; then
    wget -q "$MIFARE_DICT_URL" -O "$SD_PATH/nfc/assets/mf_classic_dict_user.nfc" 2>/dev/null && \
        echo -e "${GREEN}  [+] Dizionario MIFARE scaricato${NC}" || \
        echo -e "${YELLOW}  [!] Download dizionario fallito, continuo...${NC}"
else
    echo -e "${YELLOW}  [!] Nè curl nè wget trovati, skip download${NC}"
fi

# --- Copia payload BadUSB ---
echo ""
echo -e "${YELLOW}[4/5] Copia payload BadUSB...${NC}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYLOADS_DIR="$(dirname "$SCRIPT_DIR")/payloads"

if [ -d "$PAYLOADS_DIR" ]; then
    find "$PAYLOADS_DIR" -name "*.txt" -exec cp {} "$SD_PATH/badusb/" \;
    PAYLOAD_COUNT=$(find "$SD_PATH/badusb/" -name "*.txt" | wc -l)
    echo -e "${GREEN}  [+] $PAYLOAD_COUNT payload copiati in badusb/${NC}"
else
    echo -e "${YELLOW}  [!] Directory payloads/ non trovata, skip${NC}"
fi

# --- Copia esempi ---
echo ""
echo -e "${YELLOW}[5/5] Copia file di esempio...${NC}"

EXAMPLES_DIR="$(dirname "$SCRIPT_DIR")/examples"

if [ -d "$EXAMPLES_DIR" ]; then
    for f in "$EXAMPLES_DIR"/*.sub; do [ -f "$f" ] && cp "$f" "$SD_PATH/subghz/"; done
    for f in "$EXAMPLES_DIR"/*.nfc; do [ -f "$f" ] && cp "$f" "$SD_PATH/nfc/"; done
    for f in "$EXAMPLES_DIR"/*.rfid; do [ -f "$f" ] && cp "$f" "$SD_PATH/lfrfid/"; done
    for f in "$EXAMPLES_DIR"/*.ibtn; do [ -f "$f" ] && cp "$f" "$SD_PATH/ibutton/"; done
    for f in "$EXAMPLES_DIR"/*.ir; do [ -f "$f" ] && cp "$f" "$SD_PATH/infrared/"; done
    echo -e "${GREEN}  [+] File di esempio copiati${NC}"
else
    echo -e "${YELLOW}  [!] Directory examples/ non trovata, skip${NC}"
fi

# --- Riepilogo ---
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}[*] Setup completato!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Struttura SD card:"
echo ""
find "$SD_PATH" -maxdepth 2 -type d | head -30 | sed "s|$SD_PATH|/ext|"
echo ""
echo "Spazio utilizzato: $(du -sh "$SD_PATH" | cut -f1)"
echo ""
echo -e "${YELLOW}[!] Ricorda di:${NC}"
echo "  - Verificare che il firmware sia aggiornato"
echo "  - Controllare le frequenze Sub-GHz nel file setting_user"
echo "  - Aggiungere le tue chiavi MIFARE custom in nfc/assets/"
echo "  - Testare i payload BadUSB in VM prima di usarli in campo"
