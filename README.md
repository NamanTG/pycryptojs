# pycryptojs

> pycryptodome + CryptoJS-compatible Rijndael for non-standard key sizes.

## Install

```bash
pip install -e .
```

## What it does

`pycryptojs` is a drop-in replacement for `pycryptodome` (`Crypto.*`) that adds one extra capability:  
**AES with non-standard key sizes** (e.g. 64 bytes), matching the behavior of CryptoJS when `enc.Utf8.parse()` produces an oversized key.

Under the hood, CryptoJS follows the Rijndael spec for arbitrary key sizes:
- 64-byte key → 22 rounds (vs standard AES-256's 14 rounds)
- `pycryptodome` rejects these keys; `pycryptojs` handles them transparently.

## Usage

### Standard AES — identical to pycryptodome

```python
from pycryptojs.Cipher import AES
from pycryptojs.Util.Padding import pad, unpad

key = b'0123456789abcdef'  # 16, 24, or 32 bytes → pycryptodome handles it
iv  = b'abcdef0123456789'

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ct = cipher.encrypt(pad(b'hello world', 16))
```

### Non-standard key (e.g. 64 bytes) — Rijndael engine, ECB only

```python
from pycryptojs.Cipher import AES
from pycryptojs.Util.Padding import pad, unpad

key = b'1593cc0b7cd7651ad8a17bc528986046fa3e6e709f6405274b17def26c7faa6r'  # 64 bytes

cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(pad(b'0lrtwyvqdaj657hq4t6m', 16))
# decrypt
pt = unpad(cipher.decrypt(ct), 16)
```

### Standalone helpers (base64 in/out, PKCS7 handled internally)

```python
from pycryptojs import rijndael_ecb_encrypt, rijndael_ecb_decrypt

KEY = b'1593cc0b7cd7651ad8a17bc528986046fa3e6e709f6405274b17def26c7faa6r'

enc = rijndael_ecb_encrypt("0lrtwyvqdaj657hq4t6m", KEY)
# → "j7ywbgh7VYbTwxvei9CaRL0rNVQW7zlzeJNd+SRxUjI="

dec = rijndael_ecb_decrypt(enc, KEY)
# → "0lrtwyvqdaj657hq4t6m"
```

### Everything else — same as pycryptodome

```python
from pycryptojs.Hash import SHA256
from pycryptojs.PublicKey import RSA
from pycryptojs.Util.Padding import pad, unpad
from pycryptojs.Random import get_random_bytes
```
