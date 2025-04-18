import streamlit as st
import os
import toml

from src.utils.local_storage_manager import get_stored_theme, store_theme
from streamlit_extras.stylable_container import stylable_container

THEMES_FILE = os.path.join('.streamlit', 'themes.toml')
DEFAULT_COLORS = ["#ffffff", "#eeeeee"]
DEFAULT_TEXT_COLOR = "#ffffff"


def load_themes():
    if os.path.exists(THEMES_FILE):
        try:
            with open(THEMES_FILE, 'r') as f:
                themes = toml.load(f)
                return {k.replace('theme.', ''): v for k, v in themes.items()}
        except (toml.TomlDecodeError, OSError) as e:
            st.error(f"Failed to load themes: {e}")
    return {}


def update_theme(theme_dict):
    valid_theme_keys = {
        "primaryColor",
        "backgroundColor",
        "secondaryBackgroundColor",
        "textColor",
        "font",
    }
    for key, value in theme_dict.items():
        if key in valid_theme_keys:
            st.config.set_option(f"theme.{key}", value)  # type: ignore # noqa: SLF001


def get_theme_value(key, default=None):
    return st.session_state.get("current_theme", {}).get(key, default)


def get_back_colors():
    return [
        get_theme_value("rowAColor", DEFAULT_COLORS[0]),
        get_theme_value("rowBColor", DEFAULT_COLORS[1])
    ]


def get_text_color():
    return get_theme_value("textColor", DEFAULT_TEXT_COLOR)


# === Theme Selector UI ===
def get_section():
    themes = load_themes()
    theme_names = list(themes.keys())

    if not theme_names:
        st.sidebar.warning("No themes available.")
        return

    stored_theme = get_stored_theme()
    selected_theme = stored_theme if stored_theme in theme_names else theme_names[0]

    with st.sidebar:
        st.markdown("### Select Theme")

        cols = st.columns(len(theme_names), gap='small')
        for col, theme_name in zip(cols, theme_names):
            theme_colors = themes[theme_name]
            bg_color = theme_colors.get("secondaryBackgroundColor", "#cccccc")
            text_color = theme_colors.get("textColor", "#000000")

            css = f"""
            button {{
                background-color: {bg_color};
                color: {text_color};
                width: 100%;
            }}
            """

            with col:
                with stylable_container(theme_name, css_styles=css):
                    if st.button(theme_name.capitalize(), key=f"theme_btn_{theme_name}"):
                        selected_theme = theme_name

        # Apply theme if changed
        current_name = st.session_state.get("current_theme", {}).get("name")
        if selected_theme != current_name:
            if selected_theme in themes:
                store_theme(selected_theme)
                update_theme(themes[selected_theme])
                st.session_state.current_theme = {"name": selected_theme, **themes[selected_theme]}
                st.rerun()
