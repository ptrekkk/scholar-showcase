import streamlit as st

from src.api import db_actions
from src.models.models import User
from src.utils import local_storage_manager


def login(account):
    user = db_actions.get_user(account)
    if user:
        return user
    else:
        user = db_actions.create_user(account)
        return user


def get_user() -> User | None:
    return local_storage_manager.get_user()


def logout():
    local_storage_manager.delete_user()
    st.rerun()
