import streamlit as st
from fuzzywuzzy import fuzz
import pandas as pd
import re
import math
from collections import Counter


# Cosine similiratiy Model-----------------------------------------------------------

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


# WEB PAGE ----------------------------------------------------
st.markdown(
    "<h2 style='text-align: center; color: red;'>Fuzzy String Matching</h2>",
    unsafe_allow_html=True,
)

with st.form(key="my_form"):
    text1 = st.text_input("text1")
    text2 = st.text_input("text2")
    submit_button = st.form_submit_button("Submit")


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.write("ratio")
    st.write(fuzz.ratio(text1, text2))
with col2:
    st.write("partial_ratio")
    st.write(fuzz.partial_ratio(text1, text2))
with col3:
    st.write("token_sort_ratio")
    st.write(fuzz.token_sort_ratio(text1, text2))
with col4:
    st.write("token_set_ratio")
    st.write(fuzz.token_set_ratio(text1, text2))
with col5:
    st.write("Cosine Similarity")
    st.write(round(get_cosine(text_to_vector(text1), text_to_vector(text2)) * 100, 2))


# df_dict={'ratio':[],'partial_ratio':[],'token_sort_ratio':[],'token_set_ratio':[] }
df_dict = {}
df_dict["text1"] = text1
df_dict["text2"] = text2
df_dict["ratio"] = fuzz.ratio(text1, text2)
df_dict["partial_ratio"] = fuzz.partial_ratio(text1, text2)
df_dict["token_sort_ratio"] = fuzz.token_sort_ratio(text1, text2)
df_dict["token_set_ratio"] = fuzz.token_set_ratio(text1, text2)
df_dict["cosine"] = round(
    get_cosine(text_to_vector(text1), text_to_vector(text2)) * 100, 2
)
with open("fuzzy_data.csv", "a", encoding="utf8") as f:
    list1 = [str(item) for item in df_dict.values()]
    f.write(",".join(list1) + "\n")


df = pd.read_csv(
    "fuzzy_data.csv",
    names=[
        "text1",
        "text2",
        "ratio",
        "partial_ratio",
        "token_sort_ratio",
        "token_set_ratio",
        "cosine",
    ],
)
df = df[df["text1"].notna()]

if st.button("Clear Table"):
    with open("fuzzy_data.csv", "w", encoding="utf8") as f:
        f.write("")
    df = pd.DataFrame()

st.write(df)


st.download_button(
   "Download Table",
   df.to_csv(),
   "file.csv",
   "text/csv",
   key='download-table'
)
