"""
Extended AES module — drop-in replacement for Crypto.Cipher.AES.
Supports all standard key sizes (16, 24, 32 bytes) via pycryptodome,
AND non-standard key sizes (e.g. 64 bytes) via the custom Rijndael engine.
"""
from Crypto.Cipher import AES as _AES
from pycryptojs._rijndael import _RijndaelECB

# Re-export all mode constants and block size from pycryptodome
MODE_ECB       = _AES.MODE_ECB
MODE_CBC       = _AES.MODE_CBC
MODE_CFB       = _AES.MODE_CFB
MODE_OFB       = _AES.MODE_OFB
MODE_CTR       = _AES.MODE_CTR
MODE_CCM       = _AES.MODE_CCM
MODE_EAX       = _AES.MODE_EAX
MODE_GCM       = _AES.MODE_GCM
MODE_SIV       = _AES.MODE_SIV
MODE_OCB       = _AES.MODE_OCB
MODE_OPENPGP   = _AES.MODE_OPENPGP
MODE_KW        = _AES.MODE_KW
MODE_KWP       = _AES.MODE_KWP
block_size     = _AES.block_size
key_size       = _AES.key_size   # (16, 24, 32) — for standard AES

_STANDARD_KEY_SIZES = (16, 24, 32)


def new(key: bytes, mode: int = MODE_ECB, **kwargs):
    """
    Create an AES cipher object.

    For standard key sizes (16, 24, 32 bytes): delegates to pycryptodome.
    For non-standard key sizes (e.g. 64 bytes): uses the Rijndael engine.
    Note: non-standard keys only support MODE_ECB.

    Args:
        key:    raw key bytes
        mode:   cipher mode (default MODE_ECB)
        **kwargs: passed to pycryptodome for standard key sizes

    Returns:
        cipher object with .encrypt() and .decrypt() methods
    """
    if len(key) in _STANDARD_KEY_SIZES:
        return _AES.new(key, mode, **kwargs)

    # Non-standard key size → Rijndael engine
    if len(key) % 4 != 0:
        raise ValueError(f"Key length must be a multiple of 4 bytes, got {len(key)}")
    if mode != MODE_ECB:
        raise NotImplementedError(
            f"Non-standard key size ({len(key)} bytes) only supports MODE_ECB. "
            f"Use a 16/24/32-byte key for other modes."
        )
    return _RijndaelECB(key)
