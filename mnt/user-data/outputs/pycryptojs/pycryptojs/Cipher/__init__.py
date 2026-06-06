import importlib
import sys
from Crypto.Cipher import *  # noqa: F401, F403


def __getattr__(name):
    if name == "AES":
        mod = importlib.import_module("pycryptojs.Cipher.AES")
        sys.modules["pycryptojs.Cipher.AES"] = mod
        return mod
    try:
        mod = importlib.import_module(f"Crypto.Cipher.{name}")
        sys.modules[f"pycryptojs.Cipher.{name}"] = mod
        return mod
    except ImportError:
        raise AttributeError(f"module 'pycryptojs.Cipher' has no attribute '{name}'")
