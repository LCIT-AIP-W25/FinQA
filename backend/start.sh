#!/bin/bash
set -eo pipefail

# Configure paths
WALLET_DIR="/opt/render/project/src/wallet"
mkdir -p "$WALLET_DIR"

echo "=== Starting Wallet Setup ==="
echo "Wallet directory: $WALLET_DIR"

# ✅ Correctly decode Base64 wallet from Render's Secret File
if [ ! -f /etc/secrets/ORACLE_WALLET_BASE64 ]; then
  echo "❌ ERROR: ORACLE_WALLET_BASE64 secret file not found"
  exit 1
fi

base64 -d /etc/secrets/ORACLE_WALLET_BASE64 > "$WALLET_DIR/oracle_wallet.zip"

# Verify ZIP file
if [ ! -s "$WALLET_DIR/oracle_wallet.zip" ]; then
  echo "❌ ERROR: Wallet ZIP file is empty"
  exit 1
fi

if ! unzip -tq "$WALLET_DIR/oracle_wallet.zip"; then
  echo "❌ ERROR: Invalid ZIP file"
  file "$WALLET_DIR/oracle_wallet.zip"
  exit 1
fi

# Extract the wallet
unzip -oq "$WALLET_DIR/oracle_wallet.zip" -d "$WALLET_DIR/"

# Set strict permissions
chmod 600 "$WALLET_DIR"/*
chmod 700 "$WALLET_DIR"

# Set Oracle environment
export TNS_ADMIN="$WALLET_DIR"
echo "TNS_ADMIN set to: $TNS_ADMIN"

# Verify wallet files exist
required_files=("cwallet.sso" "sqlnet.ora" "tnsnames.ora")
for file in "${required_files[@]}"; do
  if [ ! -f "$WALLET_DIR/$file" ]; then
    echo "❌ ERROR: Missing required wallet file: $file"
    exit 1
  fi
done

# Start application
echo "=== Starting Application ==="
exec gunicorn app:app --workers=3 --worker-class=gevent --timeout 90 --bind 0.0.0.0:$PORT
