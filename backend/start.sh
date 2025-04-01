#!/bin/bash
set -eo pipefail

# Configure paths
WALLET_DIR="/opt/render/project/src/wallet"
mkdir -p "$WALLET_DIR"

echo "=== Starting Wallet Setup ==="
echo "Wallet directory: $WALLET_DIR"

# ✅ Correctly decode Base64 wallet from Render's Secret File (NOT an env var)
base64 -d /etc/secrets/ORACLE_WALLET_BASE64 > "$WALLET_DIR/oracle_wallet.zip"

# Debugging: Check file size
ls -lh "$WALLET_DIR/oracle_wallet.zip"

# Verify if it's a valid ZIP file
if ! unzip -tq "$WALLET_DIR/oracle_wallet.zip"; then
  echo "❌ ERROR: Invalid ZIP file"
  file "$WALLET_DIR/oracle_wallet.zip"
  exit 1
fi

# Extract the wallet and set permissions
unzip -oq "$WALLET_DIR/oracle_wallet.zip" -d "$WALLET_DIR/"
chmod 600 "$WALLET_DIR"/*

# Debugging: Show extracted files
echo "=== Wallet Contents ==="
ls -la "$WALLET_DIR"

# Set Oracle environment
export TNS_ADMIN="$WALLET_DIR"
echo "TNS_ADMIN set to: $TNS_ADMIN"

# Start application
echo "=== Starting Application ==="
exec gunicorn -w 3 app:app --bind 0.0.0.0:$PORT
