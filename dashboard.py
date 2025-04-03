
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import cv2
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

# Load dataset
df = pd.read_csv("inbloom_participants.csv")

# Streamlit app setup
st.set_page_config(page_title="INBLOOM '25 Dashboard", layout="wide")

# 🎨 Custom Styling
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>INBLOOM '25 Analytics Dashboard 🎭</h1>",
    unsafe_allow_html=True
)

# Sidebar for filtering
st.sidebar.header("Filter Options 🎯")
selected_event = st.sidebar.selectbox("Select Event", ["All"] + list(df["Event"].unique()))
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(df["State"].unique()))
selected_college = st.sidebar.selectbox("Select College", ["All"] + list(df["College"].unique()))

# Apply filters
filtered_df = df.copy()
if selected_event != "All":
    filtered_df = filtered_df[filtered_df["Event"] == selected_event]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
if selected_college != "All":
    filtered_df = filtered_df[filtered_df["College"] == selected_college]

# Dynamic Title Update
st.markdown(f"<h3 style='text-align: center; color: #FF9800;'>📊 Analytics for {selected_event if selected_event != 'All' else 'All Events'}</h3>", unsafe_allow_html=True)

# 📊 **1. Event-wise Participation (Bar Chart)**
st.subheader("🎭 Event-wise Participation")
fig1 = px.bar(filtered_df, x="Event", title="Event Participation", color="Event", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# 📈 **2. Participation Trend Over Days (Line Chart)**
st.subheader("📅 Daily Participation Trend")
trend_df = filtered_df.groupby("Day").size().reset_index(name="Participants")
fig2 = px.line(trend_df, x="Day", y="Participants", markers=True, title="Participation Trend")
st.plotly_chart(fig2, use_container_width=True)

# 🎂 **3. Gender Distribution (Pie Chart)**
st.subheader("⚤ Gender Distribution")
gender_df = filtered_df["Gender"].value_counts().reset_index()
gender_df.columns = ["Gender", "Count"]
fig3 = px.pie(gender_df, values="Count", names="Gender", title="Gender Ratio", hole=0.4)
st.plotly_chart(fig3, use_container_width=True)

# 🏆 **4. College Participation (Treemap)**
st.subheader("🏫 College-wise Participation")
fig5 = px.treemap(filtered_df, path=["College"], title="Participation by College", color="College")
st.plotly_chart(fig5, use_container_width=True)

# 📊 **5. Age Distribution (Histogram)**
st.subheader("📊 Age Distribution of Participants")
if "Age" in filtered_df.columns:
    fig6 = px.histogram(filtered_df, x="Age", nbins=15, title="Age Distribution of Participants", color_discrete_sequence=["#FF5733"])
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.error("⚠️ Age column not found in the dataset!")

# 📝 **6. Feedback Sentiment Analysis (Task 7)**
st.subheader("📝 Participant Feedback Analysis")
if "Feedback" in df.columns:
    feedback_texts = " ".join(df["Feedback"].dropna())
    
    # Sentiment Analysis
    sentiments = [TextBlob(text).sentiment.polarity for text in df["Feedback"].dropna()]
    sentiment_score = sum(sentiments) / len(sentiments) if sentiments else 0

    sentiment_result = "😊 Positive" if sentiment_score > 0 else "😐 Neutral" if sentiment_score == 0 else "😢 Negative"
    st.write(f"Overall Sentiment: **{sentiment_result}** (Score: {sentiment_score:.2f})")

    # Word Cloud
    st.subheader("☁️ Word Cloud of Feedback")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(feedback_texts)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

else:
    st.error("⚠️ No Feedback column found in the dataset!")

# 📸 **7. Day-wise Image Gallery (Task 8)**
st.subheader("📷 Day-wise Event Gallery")
image_dir = "event_images"  # Folder containing images
if os.path.exists(image_dir):
    event_days = sorted(set(df["Day"].dropna()))
    selected_day = st.selectbox("Choose Event Day", event_days)

    image_files = [f for f in os.listdir(image_dir) if f.startswith(f"day_{selected_day}_")]
    
    if image_files:
        cols = st.columns(3)
        for idx, image in enumerate(image_files):
            with cols[idx % 3]:
                st.image(os.path.join(image_dir, image), caption=f"Day {selected_day} Event", use_column_width=True)
    else:
        st.info("No images found for this day.")
else:
    st.error("⚠️ Image directory not found. Please upload event images.")

# 🖼️ **8. Custom Image Processing (Task 8)**
st.subheader("🛠️ Upload & Process Image")

uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    img_array = np.array(image)
    
    # Display original image
    st.image(image, caption="Original Image", use_column_width=True)

    # Select Image Processing Option
    option = st.radio("Choose Processing Type", ["Grayscale", "Edge Detection", "Blur"])

    if option == "Grayscale":
        processed_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        st.image(processed_img, caption="Grayscale Image", use_column_width=True, channels="GRAY")
    
    elif option == "Edge Detection":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        processed_img = cv2.Canny(gray, 50, 150)
        st.image(processed_img, caption="Edge Detected Image", use_column_width=True, channels="GRAY")
    
    elif option == "Blur":
        processed_img = cv2.GaussianBlur(img_array, (15, 15), 0)
        st.image(processed_img, caption="Blurred Image", use_column_width=True)

# 📌 Footer
st.markdown(
    "<h5 style='text-align: center;'>📊 Interactive Insights for INBLOOM '25 🎉</h5>",
    unsafe_allow_html=True
)


