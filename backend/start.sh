#!/bin/bash
set -e

# Use Render's persistent storage path instead of /opt
WALLET_DIR="/opt/render/project/src/wallet"
mkdir -p $WALLET_DIR
echo "$ORACLE_WALLET_BASE64" | base64 --decode > $WALLET_DIR/oracle_wallet.zip
unzip -o $WALLET_DIR/oracle_wallet.zip -d $WALLET_DIR/
chmod 600 $WALLET_DIR/*

export TNS_ADMIN=$WALLET_DIR
exec gunicorn -w 3 app:app --bind 0.0.0.0:$PORT