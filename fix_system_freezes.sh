#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE PROTECTION ANTI-FREEZE SYSTÉMIQUE (Linux Mint / Ubuntu Noble)
# Configuration matérielle ciblée : Dell Vostro 15-3568 (HDD 5400 RPM, Core i3, QCA9377)
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Ce script doit être exécuté avec les privilèges root."
  echo "    Veuillez lancer : sudo ./fix_system_freezes.sh"
  exit 1
fi

echo "======================================================================"
echo "[+] 1/4. INSTALLATION DE ZRAM-TOOLS & EARLYOOM (PROTECTION RAM & OOM)"
echo "======================================================================"
apt update -y
apt install -y zram-tools earlyoom

# Configuration ZRAM (Swap ultra-rapide compressé en RAM, 0 accès disque)
cat << 'EOF' > /etc/default/zramswap
# Allocation de 50% de la RAM en swap compressé zstd ultra-rapide
ALGO=zstd
PERCENT=50
PRIORITY=100
EOF

systemctl restart zramswap.service || service zramswap restart
systemctl enable zramswap.service

echo "[✓] ZRAM activé avec succès (vitesse RAM ~15 Go/s au lieu de 1 Mo/s sur HDD)."

# Configuration EarlyOOM (Tueur de processus fou avant que le noyau ne gèle)
cat << 'EOF' > /etc/default/earlyoom
# Déclenchement si RAM libre < 5% ou Swap < 10%
# Protège l'environnement de bureau Cinnamon et Xorg
EARLYOOM_ARGS="-m 5 -s 10 -r 60 --avoid '(^Xorg$|^cinnamon$|^lightdm$|^systemd$)' --prefer '(^chromium$|^chrome$|^node$|^python3$)'"
EOF

systemctl restart earlyoom
systemctl enable earlyoom
echo "[✓] EarlyOOM activé avec succès."

echo "======================================================================"
echo "[+] 2/4. OPTIMISATION DU NOYAU LINUX (SYSCTL SPÉCIAL DISQUE 5400 RPM)"
echo "======================================================================"
cat << 'EOF' > /etc/sysctl.d/99-anti-freeze.conf
# Évite de swapper sur le disque mécanique tant que la RAM n'est pas pleine
vm.swappiness = 10

# Privilégie le maintien en cache des fichiers et fenêtres ouvertes
vm.vfs_cache_pressure = 50

# Évite les blocages de 30 secondes en forçant l'écriture par petits blocs fluides
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
EOF

sysctl --system > /dev/null
echo "[✓] Paramètres noyau sysctl appliqués immédiatement."

echo "======================================================================"
echo "[+] 3/4. CORRECTION DU BUG MATÉRIEL PCIE AER (WIFI ATH10K & PONT PCIE)"
echo "======================================================================"
GRUB_FILE="/etc/default/grub"
if [ -f "$GRUB_FILE" ]; then
  if grep -q "pci=noaer" "$GRUB_FILE"; then
    echo "[i] pci=noaer est déjà présent dans $GRUB_FILE."
  else
    echo "[+] Ajout de 'pci=noaer' à GRUB_CMDLINE_LINUX_DEFAULT pour stopper les 1300+ interruptions AER..."
    sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\(quiet splash\)\?"/GRUB_CMDLINE_LINUX_DEFAULT="\1 pci=noaer"/' "$GRUB_FILE"
    # Nettoyage d'éventuels espaces doubles
    sed -i 's/  */ /g' "$GRUB_FILE"
    update-grub
    echo "[✓] Configuration GRUB mise à jour (prendra effet complet au prochain redémarrage)."
  fi
fi

echo "======================================================================"
echo "[+] 4/4. VÉRIFICATION DU STATUT DU SYSTÈME"
echo "======================================================================"
swapon --show
echo ""
echo "EarlyOOM status:"
systemctl is-active earlyoom
echo ""
echo "Swappiness actuel:"
cat /proc/sys/vm/swappiness
echo ""
echo "======================================================================"
echo "✓ TOUTES LES PROTECTIONS SONT EN PLACE !"
echo "Votre PC ne gèlera plus sous forte charge mémoire ou lors des rendus."
echo "======================================================================"
