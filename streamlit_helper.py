import base64
import streamlit.components.v1 as components
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("data:image/png;base64,%s");
      background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

#@st.cache(suppress_st_warning=True)
def deloy_html(path, height, width):
    HtmlFile = open(path, 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    return components.html(source_code, height = height, width = width, scrolling=True)

#@st.cache(suppress_st_warning=True)
def explainatory_text(title, string):
    new_title = '<p style="font-family:sans-serif; color:#33B5F6; font-size: 42px;">' +  title + ' </p>'
    st.markdown(new_title, unsafe_allow_html=True)
    t = "<font color='#33B5F6'>" +  string + "</font>"
    st.markdown(t, unsafe_allow_html=True)
    st.write()  
    return