import streamlit as st

st.markdown("*Streamlit* é **realmente** ***legal***.")
st.markdown("""
    :red[Streamlit] :orange[pode] :green[escrever] :blue[texto] :violet[em]
    :gray[belas] :rainbow[cores] e texto :blue-background[destacado].
""")
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = """If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
"""
st.markdown(multi)
