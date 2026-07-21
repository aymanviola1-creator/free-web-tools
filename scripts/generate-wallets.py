"""
Generate REAL cryptocurrency wallets for receiving payments.
Each wallet is generated with a cryptographically secure private key.
Save the private keys securely - they control access to the funds.

Output: data/wallets.json (PUBLIC addresses only - safe to share)
Output: data/wallets-private.json (SECRET - keep safe!)
"""

import json
import os
import secrets
import hashlib
import base64

WALLETS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "wallets.json")
PRIVATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "wallets-private.json")

print("=" * 60)
print("  CRYPTO WALLET GENERATOR")
print("  Generating real wallets for receiving payments")
print("=" * 60)

wallets = {}
private_wallets = {}

# ============================================================
# 1. BITCOIN WALLET
# ============================================================
print("\n[1/4] Generating Bitcoin wallet...")
try:
    from bitcoinlib.keys import Key
    btc_key = Key()
    wallets["BTC"] = {
        "address": btc_key.address(),
        "network": "bitcoin",
    }
    private_wallets["BTC"] = {
        "address": btc_key.address(),
        "private_key_wif": btc_key.wif(),
        "private_key_hex": btc_key.private_hex,
    }
    print(f"  ✅ BTC Address: {btc_key.address()}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    wallets["BTC"] = {"address": "bc1qplaceholder", "network": "bitcoin", "note": "Generate failed"}
    private_wallets["BTC"] = {"address": "bc1qplaceholder", "note": "Generation failed"}

# ============================================================
# 2. ETHEREUM WALLET
# ============================================================
print("\n[2/4] Generating Ethereum wallet...")
try:
    from eth_account import Account
    
    private_key_hex = "0x" + secrets.token_hex(32)
    acct = Account.from_key(private_key_hex)
    
    wallets["ETH"] = {
        "address": acct.address,
        "network": "ethereum",
    }
    private_wallets["ETH"] = {
        "address": acct.address,
        "private_key": private_key_hex,
    }
    print(f"  ✅ ETH Address: {acct.address}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    wallets["ETH"] = {"address": "0xplaceholder", "network": "ethereum", "note": "Generation failed"}
    private_wallets["ETH"] = {"address": "0xplaceholder", "note": "Generation failed"}

# ============================================================
# 3. SOLANA WALLET
# ============================================================
print("\n[3/4] Generating Solana wallet...")
try:
    from solders.keypair import Keypair
    import base58
    
    sol_keypair = Keypair()
    sol_pubkey = str(sol_keypair.pubkey())
    sol_secret = base58.b58encode(bytes(sol_keypair)).decode()
    
    wallets["SOL"] = {
        "address": sol_pubkey,
        "network": "solana",
    }
    private_wallets["SOL"] = {
        "address": sol_pubkey,
        "private_key_base58": sol_secret,
    }
    print(f"  ✅ SOL Address: {sol_pubkey}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    wallets["SOL"] = {"address": "SoLplaceholder", "network": "solana", "note": "Generation failed"}
    private_wallets["SOL"] = {"address": "SoLplaceholder", "note": "Generation failed"}

# ============================================================
# 4. TON WALLET (Simplified - use Tonkeeper for real wallet)
# ============================================================
print("\n[4/4] TON wallet info...")
# For TON, we generate an Ed25519 keypair that can be imported into Tonkeeper
try:
    from nacl.bindings import crypto_sign_seed_keypair
    
    ton_seed = os.urandom(32)
    ton_pk, ton_sk = crypto_sign_seed_keypair(ton_seed)
    
    # The public key is the TON wallet identifier
    pub_key_hex = bytes(ton_pk).hex()
    
    wallets["TON"] = {
        "address": f"ton://wallet/{pub_key_hex}",
        "public_key_hex": pub_key_hex,
        "network": "ton",
        "note": "Create a TON wallet in Tonkeeper app, then use its receive address"
    }
    private_wallets["TON"] = {
        "public_key_hex": pub_key_hex,
        "seed_hex": ton_seed.hex(),
        "private_key_hex": bytes(ton_sk).hex(),
        "note": "This keypair can be imported into TON-compatible wallets"
    }
    print(f"  ✅ TON keypair generated (public key: {pub_key_hex[:16]}...)")
    print(f"     📱 For TON payments: Install Tonkeeper app and get your receive address")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    wallets["TON"] = {
        "address": "EQD-install-tonkeeper",
        "network": "ton",
        "note": "Install Tonkeeper app to generate a TON wallet"
    }
    private_wallets["TON"] = {"note": "Use Tonkeeper app to generate a TON wallet"}

# ============================================================
# SAVE WALLETS
# ============================================================
print("\n" + "=" * 60)
print("  SAVING WALLETS")
print("=" * 60)

os.makedirs(os.path.dirname(WALLETS_FILE), exist_ok=True)

# Save PUBLIC addresses only (safe to share)
with open(WALLETS_FILE, 'w') as f:
    json.dump(wallets, f, indent=2)
print(f"  ✅ Public addresses saved to: {WALLETS_FILE}")

# Save PRIVATE keys (SECRET - do not share!)
with open(PRIVATE_FILE, 'w') as f:
    json.dump(private_wallets, f, indent=2)
print(f"  🔐 Private keys saved to: {PRIVATE_FILE}")
print(f"  ⚠️  WARNING: KEEP PRIVATE KEYS SECURE!")
print(f"  ⚠️  Anyone with private keys controls the funds.")

print("\n" + "=" * 60)
print("  SUMMARY - Public Addresses for Payments")
print("=" * 60)
for currency, info in wallets.items():
    print(f"  {currency}: {info['address']}")

print("\n✅ Wallet generation complete!")
print("   Add these addresses to your websites, GitHub repos, and tools.")
print("   The private keys file (wallets-private.json) is needed to withdraw funds.")
print()
print("   💡 NEXT STEPS FOR THE HUMAN:")
print("   1. Open wallets-private.json, save the private keys securely")
print("   2. Import BTC key into Electrum or any Bitcoin wallet")
print("   3. Import ETH key into MetaMask or MyEtherWallet")
print("   4. Import SOL key into Phantom or Solflare wallet")
print("   5. Get TON address from Tonkeeper app")
print("   6. Start accepting payments!")
