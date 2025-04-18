import json
import base64
import logging
from time import sleep

import streamlit as st
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from streamlit_local_storage import LocalStorage

from src.models.models import User

WAIT_AFTER_STORE = 0.8

secret = st.secrets["cookies"]["password"]

log = logging.getLogger("LocalStorage")


def _get_aes_cipher(secret_key: str, salt: bytes):
    key = PBKDF2(secret_key, salt, dkLen=32)
    return key


def encrypt_data(data: str, password: str) -> str:
    salt = get_random_bytes(16)
    key = _get_aes_cipher(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    encrypted_blob = salt + cipher.nonce + tag + ciphertext
    return base64.b64encode(encrypted_blob).decode()


def decrypt_data(enc_data_b64: str, password: str) -> str:
    try:
        enc = base64.b64decode(enc_data_b64)
        salt, nonce, tag, ciphertext = enc[:16], enc[16:32], enc[32:48], enc[48:]
        key = _get_aes_cipher(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
    except Exception as e:
        st.error(f"Decryption failed: {e}")
        return ""


def get_storage():
    return LocalStorage()


def save_user(user: User):
    storage = get_storage()
    encrypted = encrypt_data(json.dumps(user.to_dict()), secret)
    storage.setItem("user", encrypted)
    # Give system time before rerun
    sleep(WAIT_AFTER_STORE)


def get_user() -> User | None:
    storage = get_storage()
    encrypted = storage.getItem("user")
    if not encrypted:
        return None

    decrypted = decrypt_data(encrypted, secret)
    try:
        return User(**json.loads(decrypted))
    except Exception as e:
        log.error(f"Failed to parse user: {e}")
        delete_user()
        return None


def delete_user():
    storage = get_storage()
    storage.deleteItem("user")
    # Give system time before rerun
    sleep(WAIT_AFTER_STORE)


def get_stored_theme():
    storage = get_storage()
    theme = storage.getItem("theme")
    return theme


def store_theme(theme_name):
    storage = get_storage()
    storage.setItem("theme", theme_name)
    sleep(WAIT_AFTER_STORE)
