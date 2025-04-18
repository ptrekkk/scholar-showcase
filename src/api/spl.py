import logging
from typing import Dict, Any, Optional

import pandas as pd
import requests
import streamlit as st
from requests.adapters import HTTPAdapter

from src.api.logRetry import LogRetry

# API URLs
API_URLS = {
    "base": "https://api2.splinterlands.com/",
    "land": "https://vapi.splinterlands.com/",
    "prices": "https://prices.splinterlands.com/",
}

# Configure Logging
log = logging.getLogger("SPL API")
log.setLevel(logging.INFO)


# Retry Strategy
def configure_http_session() -> requests.Session:
    retry_strategy = LogRetry(
        total=11,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=2,
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        logger_name="SPL Retry"
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.headers.update({
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "User-Agent": "BeeBalanced/1.0"
    })
    return session


http = configure_http_session()


def fetch_api_data(address: str, params: Optional[Dict[str, Any]] = None,
                   data_key: Optional[str] = None) -> pd.DataFrame:
    """
    Generic function to fetch data from the Splinterlands API.

    :param address: API endpoint URL.
    :param params: Query parameters for the request.
    :param data_key: Key to extract data from JSON response (optional).
    :return: DataFrame with requested data or empty DataFrame on failure.
    """
    try:
        response = http.get(address, params=params, timeout=10)
        response.raise_for_status()

        response_json = response.json()

        # Handle API errors
        if isinstance(response_json, dict) and "error" in response_json:
            log.error(f"API error from {address}: {response_json['error']}")
            return None

        if data_key and isinstance(response_json, dict):
            response_json = get_nested_value(response_json, data_key)

        return response_json

    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching {address}: {e}")
        return pd.DataFrame()


def get_nested_value(response_dict: dict, key_path: str) -> Any:
    """
    Retrieve a nested value from a dictionary using dot-separated keys.
    """
    keys = key_path.split(".")
    for key in keys:
        if isinstance(response_dict, dict) and key in response_dict:
            response_dict = response_dict[key]
        else:
            log.error(f"Invalid key requested {key_path}.. Fix api call or check response changed {response_dict}")
            return {}  # Return empty if any key is missing
    return response_dict


@st.cache_data(ttl="1h")
def get_complete_tournaments():
    log.info("Get SPL tournaments")
    result = fetch_api_data(f'{API_URLS['base']}tournaments/completed', data_key='data')
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


def get_tournament(_id):
    params = {"id": _id}
    result = fetch_api_data(f'{API_URLS['base']}tournaments/find', params=params, data_key='players')
    if result:
        return pd.DataFrame(result)
    return pd.DataFrame()


def get_leaderboard_with_player(player, format_type):
    params = {
        'username': player,
        'format': format_type,
    }

    result = fetch_api_data(f'{API_URLS['base']}players/leaderboard_with_player', params=params, data_key='player')
    if result and len(result) > 1:
        return pd.DataFrame(result, index=[0])
    return pd.DataFrame()


def get_player_profile(player):
    params = {
        'name': player,
        'season_details': 'true',
        'format': 'all',
    }

    result = fetch_api_data(f'{API_URLS['base']}players/details', params=params)
    if result:
        return result
    return None
