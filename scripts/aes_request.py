#!/usr/bin/env python3
"""
szpu-api-search — AES-CBC/PKCS7 加密请求工具
用法:
  python aes_request.py login  --key <api_key> --username <u> --password <p>
  python aes_request.py score  --key <api_key> --username <u> --password <p>

AES 密钥（content）由脚本每次随机生成：16 位数字与英文字母，无需传入。
"""

import argparse
import json
import secrets
import string
import sys
import urllib.parse
import urllib.request

# pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

BASE_URL = "https://api.cloudslow.com/szpu"
IV = b"wn0ZfU4qmbhHE1lo"  # 固定 IV，16 字节
_AES_KEY_ALPHABET = string.ascii_letters + string.digits


def random_aes_key() -> str:
    """16 位随机字符串（数字 + 英文），用作 AES-128 密钥与 content 参数。"""
    return "".join(secrets.choice(_AES_KEY_ALPHABET) for _ in range(16))


def aes_encrypt(plaintext: str, key: str) -> str:
    """AES-CBC + PKCS7，返回 Base64 密文。"""
    key_bytes = key.encode("utf-8")
    cipher = AES.new(key_bytes, AES.MODE_CBC, IV)
    ct = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(ct).decode("utf-8")


def call_api(endpoint: str, payload: dict, content: str) -> dict:
    """加密 payload，发 GET 请求，返回响应 JSON。"""
    plaintext = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    encrypted_data = aes_encrypt(plaintext, content)

    params = urllib.parse.urlencode({
        "data": encrypted_data,
        "content": content,
    })
    url = f"{BASE_URL}{endpoint}?{params}"

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="SZPU API 加密请求工具")
    parser.add_argument("action", choices=["login", "score"], help="login=searchLogin, score=searchScore")
    parser.add_argument("--key", required=True, help="API 密钥 (key_value)")
    parser.add_argument("--username", required=True, help="学号/账号")
    parser.add_argument("--password", required=True, help="密码")
    args = parser.parse_args()

    content = random_aes_key()

    payload = {
        "key": args.key,
        "data": {
            "username": args.username,
            "password": args.password,
        }
    }

    endpoint = "/api/searchLogin" if args.action == "login" else "/api/searchScore"
    print(f"→ 调用 {endpoint} ...")

    try:
        result = call_api(endpoint, payload, content)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
