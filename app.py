import streamlit as st
import pickle
import numpy as np

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="📚 BookVerse by Shagun",
    page_icon="📚",
    layout="wide"
)

# ---------------- Load Files ---------------- #

pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background: linear-gradient(to right,#0f172a,#1e293b);
}

h1{
    text-align:center;
    color:white;
}

h4{
    color:white;
}

div.stButton > button{
    width:100%;
    height:55px;
    background:linear-gradient(90deg,#7c3aed,#2563eb);
    color:white;
    border:none;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:linear-gradient(90deg,#2563eb,#7c3aed);
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ---------------- #

st.markdown(
    "<h1>📚 BookVerse by Shagun</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;color:#cbd5e1;'>Discover your next favourite book ✨</h4>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

# ---------------- Recommendation Function ---------------- #

def recommend(book_name):

    index = np.where(pt.index == book_name)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []

    for i in similar_items:

        temp_df = books[
            books["Book-Title"] == pt.index[i[0]]
        ].drop_duplicates("Book-Title")

        item = []

        item.append(temp_df["Book-Title"].values[0])

        item.append(temp_df["Book-Author"].values[0])

        image_url = temp_df["Image-URL-M"].values[0]

        # http -> https (images ke liye)
        if isinstance(image_url, str):
            image_url = image_url.replace("http://", "https://")

        item.append(image_url)

        data.append(item)

    return data

# ---------------- Select Box ---------------- #

selected_book = st.selectbox(
    "🔍 Search / Select a Book",
    pt.index.values
)

# ---------------- Button ---------------- #

if st.button("✨ Recommend Books"):

    recommendations = recommend(selected_book)

    st.write("")
    st.subheader("📖 You may also like")

    cols = st.columns(5)

    for idx, book in enumerate(recommendations):

        with cols[idx]:

            st.image(book[2], use_container_width=True)

            st.markdown(
                f"""
                <div style="
                background:#1e293b;
                padding:12px;
                border-radius:12px;
                margin-top:8px;
                min-height:130px;
                text-align:center;
                ">

                <h5 style="color:white;">
                {book[0]}
                </h5>

                <p style="color:#cbd5e1;">
                {book[1]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )