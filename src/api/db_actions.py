import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from src.models.models import User, RoleEnum

# Setup the engine and session factory
db_url = st.secrets["database"]["url"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Context manager for session
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Function to get a single user
def get_user(username: str) -> User | None:
    with get_session() as session:
        return session.query(User).filter_by(account=username).first()

# Function to create a new user
def create_user(username: str) -> User:
    with get_session() as session:
        new_user = User(
            account=username,
            role=RoleEnum.Undefined,
            discord_reference=None,
            preferred_mode=None,
            reward_split=None,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

# Function to update an existing user
def update_user(user: User) -> User:
    with get_session() as session:
        updated_user = session.merge(user)
        session.commit()
        session.refresh(updated_user)
        return updated_user

# Convert users to DataFrame
def users_to_df(users) -> pd.DataFrame:
    if not users:
        return pd.DataFrame(columns=[
            "account",
            "role",
            "discord_reference",
            "preferred_mode",
            "preferred_league",
            "reward_split"
        ])

    if not isinstance(users, list):
        users = [users]

    return pd.DataFrame([user.to_dict() for user in users])

# Get all managers
def get_all_managers():
    with get_session() as session:
        stmt = select(User).where(User.role == RoleEnum.Manager)
        managers = session.scalars(stmt).all()
        return users_to_df(managers)

# Get all scholars
def get_all_scholars():
    with get_session() as session:
        stmt = select(User).where(User.role == RoleEnum.Scholar)
        scholars = session.scalars(stmt).all()
        return users_to_df(scholars)

# Get specific scholar by account
def get_scholar(account):
    with get_session() as session:
        stmt = select(User).where(and_(User.role == RoleEnum.Scholar, User.account == account))
        scholar = session.scalar(stmt)
        return users_to_df(scholar)
