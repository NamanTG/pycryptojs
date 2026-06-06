"""
pycryptojs — pycryptodome + CryptoJS-compatible Rijndael for non-standard key sizes.

Drop-in replacement for pycryptodome (Crypto.*) with two extras:
    - pycryptojs.Cipher.AES.new() auto-detects oversized keys and routes to Rijndael
    - rijndael_ecb_encrypt() / rijndael_ecb_decrypt() as standalone functions

Usage:
    # Standard AES (delegates to pycryptodome)
    from pycryptojs.Cipher import AES
    from pycryptojs.Util.Padding import pad, unpad
    cipher = AES.new(key_32, AES.MODE_CBC, iv=iv)

    # Non-standard key (64 bytes) — Rijndael engine, ECB only
    cipher = AES.new(key_64, AES.MODE_ECB)
    ct = cipher.encrypt(padded_data)

    # Standalone helpers (base64 in/out, PKCS7 handled internally)
    from pycryptojs import rijndael_ecb_encrypt, rijndael_ecb_decrypt
    enc = rijndael_ecb_encrypt("hello", key_64)
    dec = rijndael_ecb_decrypt(enc, key_64)
"""

import sys
import importlib
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec

from Crypto import *  # noqa: F401, F403
from Crypto import Random, Util

from pycryptojs._rijndael import rijndael_ecb_encrypt, rijndael_ecb_decrypt


class _PycryptojsLoader(Loader):
    def __init__(self, crypto_name):
        self._crypto_name = crypto_name

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        real = importlib.import_module(self._crypto_name)
        module.__dict__.update(real.__dict__)
        module.__dict__["__name__"] = module.__name__
        sys.modules[self._crypto_name] = real


class _PycryptojsFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if not fullname.startswith("pycryptojs."):
            return None
        # Let pycryptojs.Cipher.AES resolve to our real file
        if fullname == "pycryptojs.Cipher.AES":
            return None
        # Everything else: proxy to Crypto.*
        crypto_name = "Crypto" + fullname[len("pycryptojs"):]
        try:
            importlib.import_module(crypto_name)
        except ImportError:
            return None
        return ModuleSpec(fullname, _PycryptojsLoader(crypto_name))


if not any(isinstance(f, _PycryptojsFinder) for f in sys.meta_path):
    sys.meta_path.append(_PycryptojsFinder())


__version__ = "1.0.0"
__all__ = [
    "rijndael_ecb_encrypt",
    "rijndael_ecb_decrypt",
    "Cipher", "Hash", "PublicKey", "Signature",
    "Util", "IO", "Protocol", "Random", "Math",
]
