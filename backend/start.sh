#!/bin/bash

# 1. Fail immediately if any command fails
set -e

# 2. Set up the Oracle Wallet
mkdir -p /opt/wallet
echo "$ORACLE_WALLET_BASE64" | base64 --decode > /opt/wallet/oracle_wallet.zip
unzip -o /opt/wallet/oracle_wallet.zip -d /opt/wallet/
chmod 600 /opt/wallet/* 

# 3. Configure Oracle Environment
export TNS_ADMIN=/opt/wallet  

# 4. Start Gunicorn with your app
exec gunicorn -w 3 app:app --bind 0.0.0.0:10000