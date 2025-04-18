import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.models.models import User, RoleEnum

db_url = st.secrets["database"]["url"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
db = Session()


def get_user(username: str) -> User | None:
    return db.query(User).filter_by(account=username).first()


def create_user(username: str) -> User:
    new_user = User(
        account=username,
        role=RoleEnum.Undefined,
        discord_reference=None,
        preferred_mode=None,
        reward_split=None,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(user: User) -> User:
    updated_user = db.merge(user)
    db.commit()
    db.refresh(updated_user)
    return updated_user


def users_to_df(users) -> pd.DataFrame:
    if users:
        return pd.DataFrame([user.to_dict() for user in users])
    else:
        return pd.DataFrame(columns=[
            "account",
            "role",
            "discord_reference",
            "preferred_mode",
            "preferred_league",
            "reward_split"
        ])


def get_all_managers():
    stmt = select(User).where(User.role == RoleEnum.Manager)
    managers = db.scalars(stmt).all()
    return users_to_df(managers)


def get_all_scholars():
    stmt = select(User).where(User.role == RoleEnum.Scholar)
    scholars = db.scalars(stmt).all()
    return users_to_df(scholars)
