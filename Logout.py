import json
from pathlib import Path

# Setup
import streamlit as st
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page
from auth0_component import login_button

domain = st.secrets['domain']
clientId = st.secrets['clientId']
auth0_client_secret = st.secrets['auth0_client_secret']

DEFAULT_PAGE = "Logout.py"
SECOND_PAGE_NAME = "Welcome"

st.set_page_config( 
     page_title="iDoc", 
     page_icon="🏫", 
 ) 
st.snow()
def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()
            break


clear_all_but_first_page()

st.session_state["username"]="User"

# Main function
def main():
    # """Login page"""
    logged_in = True
    hide_default_format = """ 
        <style> 
        #MainMenu {visibility: show; } 
        footer {visibility: hidden;} 
        </style> 
        """ 
    st.markdown(hide_default_format, unsafe_allow_html=True) 

    def gradient_text(text, color1, color2):
        gradient_css = f"""
        background: -webkit-linear-gradient(left, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 42px;
        """
        return f'<span style="{gradient_css}">{text}</span>'

    color1 = "#0d3270"
    color2 = "#0fab7b"
    text = "HealthOracle"
  
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("images/logo.png", width=200)

    styled_text = gradient_text(text, color1, color2)
    st.write(f"<div style='text-align: center;'>{styled_text}</div>", unsafe_allow_html=True)
    
    st.markdown(""" 
        ####  Decode Your Health with iDoc

        1. **Kidney Lens**

        2. **Brain Lens**
   
        3. **Lung Lens**
   
        4. **Tuberculosis predictor**
                """)

    st.markdown(
        "<h10 style='text-align: left; color: #ffffff;'> If you do not have an account, create an accouunt by select SignUp option.</h10>",
        unsafe_allow_html=True,
    )


    user_info=login_button(clientId, domain = domain)
    st.write(logged_in)
    if user_info:
        st.session_state["username"]=user_info["name"]
        logged_in = True

        st.success("Logged In as {}".format(user_info["name"]))

        if st.success:
            st.subheader("User Detail")
            st.write(user_info)
                   
        else:
            st.warning("Incorrect Username/Password")
    
    if logged_in:
        show_all_pages()
        # hide_page(DEFAULT_PAGE.replace(".py", ""))
        logged_in=False
        user_info=""
        switch_page('Welcome')
    else:
        clear_all_but_first_page()

if __name__ == "__main__":
    main()
