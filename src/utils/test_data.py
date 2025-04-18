import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api import db_actions
from src.models.models import User, RoleEnum, PreferredModesEnum, PreferredLeagueEnum, RewardSplitEnum

db_url = st.secrets["database"]["url"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
db = Session()


def add_dummy_users():
    add_user(
        "test_manager",
        RoleEnum.Manager,
        None,
        None,
        None,
        None
    )
    add_user(
        "test_manager1",
        RoleEnum.Manager,
        "DummyDiscord",
        None,
        None,
        None
    )
    add_user("scholar_1",
             RoleEnum.Scholar,
             "Dummy Scholar",
             PreferredModesEnum.Any,
             PreferredLeagueEnum.Gold,
             RewardSplitEnum.SPS_25_75
             )
    add_user("kvm86",
             RoleEnum.Scholar,
             "Dummy Scholar (kvm86)",
             PreferredModesEnum.Any,
             PreferredLeagueEnum.Gold,
             RewardSplitEnum.Negotiable
             )
    add_user("jerwin2022",
             RoleEnum.Scholar,
             "Dummy Scholar (jerwin2022)",
             PreferredModesEnum.Any,
             PreferredLeagueEnum.Diamond,
             RewardSplitEnum.SPS_75_25
             )


def user_exists(name):
    return True if db_actions.get_user(name) else False


def add_user(name, role, discord, preferred_mode, preferred_league, reward_split):
    if not user_exists(name):
        new_user = User(
            account=name,
            role=role,
            discord_reference=discord,
            preferred_league=preferred_league,
            preferred_mode=preferred_mode,
            reward_split=reward_split,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
