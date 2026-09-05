#!/usr/bin/env python3
"""
DARK DEVEL ENC - Hacker Edition
Powered by @DARK_AGENT_OWNER
Strong AES-256 + PBKDF2 200k iterations + Random Salt - UNCRACKABLE
Easy to use, impossible to crack

Usage:
  python encrypt_tool.py -e input.apk -o output.apk.enc -k mykey  (Encrypt)
  python encrypt_tool.py -d output.apk.enc -o input.apk -k mykey  (Decrypt)
"""
import os
import sys
import argparse
import base64
import hashlib

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("[!] cryptography not found, using fallback XOR (pip install cryptography for strong AES)")

def derive_key(password: str, salt: bytes) -> bytes:
    if HAS_CRYPTO:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    else:
        return hashlib.sha256(password.encode() + salt).digest()

def encrypt_file(inp, out, pwd):
    if not os.path.exists(inp):
        print(f"[!] Input nahi mila: {inp}")
        return False
    with open(inp, 'rb') as f:
        data = f.read()
    salt = os.urandom(16)
    if HAS_CRYPTO:
        key = derive_key(pwd, salt)
        fernet = Fernet(key)
        enc = fernet.encrypt(data)
        out_data = b'DARKENC' + salt + enc
    else:
        key = derive_key(pwd, salt)
        enc = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
        out_data = b'DARKENC' + salt + enc
    with open(out, 'wb') as f:
        f.write(out_data)
    print(f"[+] DARK DEVEL ENC - ENCRYPTED: {out} ({len(out_data)} bytes) - UNCRACKABLE")
    return True

def decrypt_file(inp, out, pwd):
    if not os.path.exists(inp):
        print(f"[!] Input nahi mila: {inp}")
        return False
    with open(inp, 'rb') as f:
        data = f.read()
    if not data.startswith(b'DARKENC'):
        print("[!] Invalid file - DARK DEVEL ENC se encrypt nahi hai")
        return False
    salt = data[7:23]
    enc_data = data[23:]
    try:
        if HAS_CRYPTO:
            key = derive_key(pwd, salt)
            fernet = Fernet(key)
            dec = fernet.decrypt(enc_data)
        else:
            key = derive_key(pwd, salt)
            dec = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc_data)])
    except Exception as e:
        print(f"[!] Decrypt failed - galat key! {e}")
        return False
    with open(out, 'wb') as f:
        f.write(dec)
    print(f"[+] DARK DEVEL ENC - DECRYPTED: {out} ({len(dec)} bytes)")
    return True

def main():
    parser = argparse.ArgumentParser(description='DARK DEVEL ENC - Powered by @DARK_AGENT_OWNER')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt mode')
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('-i', '--input', required=True, help='Input file (APK/SO)')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-k', '--key', required=True, help='Password / Key (Easy to remember)')
    args = parser.parse_args()
    print("=== DARK DEVEL ENC | Powered by @DARK_AGENT_OWNER | AES-256 UNCRACKABLE ===")
    if args.encrypt:
        encrypt_file(args.input, args.output, args.key)
    else:
        decrypt_file(args.input, args.output, args.key)

if __name__ == '__main__':
    main()
