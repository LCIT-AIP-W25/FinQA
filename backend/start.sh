#!/bin/bash
set -eo pipefail

# Configure paths
WALLET_DIR="/opt/render/project/src/wallet"
mkdir -p "$WALLET_DIR"

# Debug info
echo "=== Starting Wallet Setup ==="
echo "Working directory: $(pwd)"
echo "Wallet directory: $WALLET_DIR"

# Base64 decode with validation
echo "$ORACLE_WALLET_BASE64" | base64 -di > "$WALLET_DIR/oracle_wallet.zip"

# Verify and extract
if ! unzip -tq "$WALLET_DIR/oracle_wallet.zip"; then
  echo "❌ ERROR: Invalid ZIP file"
  file "$WALLET_DIR/oracle_wallet.zip"
  exit 1
fi

unzip -oq "$WALLET_DIR/oracle_wallet.zip" -d "$WALLET_DIR/"
chmod 600 "$WALLET_DIR"/*

# Verify extracted files
echo "=== Wallet Contents ==="
ls -la "$WALLET_DIR"

# Set Oracle environment
export TNS_ADMIN="$WALLET_DIR"
echo "TNS_ADMIN set to: $TNS_ADMIN"

# Start application
echo "=== Starting Application ==="
exec gunicorn -w 3 app:app --bind 0.0.0.0:$PORT