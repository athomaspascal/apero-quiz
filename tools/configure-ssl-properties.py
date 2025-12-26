#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration automatique de SSL dans application.properties
"""

import shutil
from datetime import datetime

print("="*70)
print("  CONFIGURATION SSL DANS application.properties")
print("="*70)
print()

properties_file = 'src/main/resources/application.properties'

# Backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'{properties_file}.backup_ssl_{timestamp}'
shutil.copy(properties_file, backup_file)
print(f"[OK] Backup cree: {backup_file}")
print()

# Lire le fichier actuel
with open(properties_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Nouvelles lignes SSL à ajouter
ssl_config = """
# ============================================================
# SSL/HTTPS Configuration
# ============================================================
# HTTPS Port (443 standard, 8443 pour dev)
server.port=8443

# SSL Enabled
server.ssl.enabled=true

# Keystore Configuration
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=quiz-app-2025
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=quiz-app

# SSL Protocol
server.ssl.protocol=TLS
server.ssl.enabled-protocols=TLSv1.2,TLSv1.3

# Force HTTPS
security.require-ssl=true

"""

# Modifier les lignes
new_lines = []
ssl_section_added = False
skip_next_blank = False

for i, line in enumerate(lines):
    # Commenter l'ancien port
    if line.strip().startswith('server.port=8089'):
        new_lines.append('#' + line)
        if not ssl_section_added:
            new_lines.append(ssl_config)
            ssl_section_added = True
            skip_next_blank = True
    # Garder les autres lignes
    elif not (skip_next_blank and line.strip() == ''):
        new_lines.append(line)
        skip_next_blank = False

# Si la section SSL n'a pas été ajoutée (port déjà commenté), l'ajouter à la fin
if not ssl_section_added:
    # Chercher après server.address
    for i, line in enumerate(new_lines):
        if 'server.address' in line:
            # Insérer après cette ligne
            new_lines.insert(i + 1, ssl_config)
            ssl_section_added = True
            break

# Écrire le fichier modifié
with open(properties_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("[OK] Fichier application.properties mis a jour")
print()
print("Modifications apportees:")
print("  - Port change: 8089 (HTTP) -> 8443 (HTTPS)")
print("  - SSL active: server.ssl.enabled=true")
print("  - Keystore: classpath:keystore.p12")
print("  - Protocoles: TLSv1.2, TLSv1.3")
print()
print("="*70)
print("[SUCCESS] Configuration SSL terminee!")
print("="*70)
print()
print("Prochaine etape:")
print("  1. Generer le certificat: generate-ssl-cert.bat")
print("  2. Configurer le pare-feu (Admin): configure-firewall-8443.bat")
print("  3. Demarrer l'app: start_clean.bat")
print("  4. Acceder via: https://192.168.1.90:8443")
print()

