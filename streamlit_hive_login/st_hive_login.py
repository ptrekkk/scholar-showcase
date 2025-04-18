import os
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "hive_login",
    path=os.path.join(os.path.dirname(__file__), "frontend/build")
)


def st_hive_login():
    return _component_func(default=None)
