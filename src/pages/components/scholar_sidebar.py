import streamlit as st


image = ("https://files.peakd.com/file/peakd-hive/beaker007"
         "/AKU4rURK8P2pc8f8Kx51xfZ1gTtM9jx8bci3PtauZuJor1kpuGAGhrFEWxvRcwC.png")


def add_scholar_img():
    with st.sidebar:
        st.markdown(
            f"""
            <style>
                .custom-sidebar-img {{
                    height: 200px;
                    border-radius: 12px;
                    display: inline-block;
                    margin-top: 1rem;
                }}
            </style>

            <div style="padding: 1rem; text-align: center;">
                <img class="custom-sidebar-img" src="{image}" />
            </div>
            """,
            unsafe_allow_html=True
        )
