import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import base64  
import webbrowser  

st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.markdown("By Shivam Sharma ([Portfolio](https://shivamshi.github.io/portfolio))👈")

# Add empty text elements to create a gap
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")

st.sidebar.markdown("Don't have the file to text currently?\nWell, no worries, I got you.\nDownload this Random Chat file to test this app⬇️")

if st.sidebar.button("Random Chat"):
    text_content = "This is the content of RandomChat.txt."
    href = f"data:text/plain;base64,{base64.b64encode(text_content.encode()).decode()}"
    st.sidebar.markdown(
        f'<a href="{href}" download="RandomChat.txt">Click here to download</a>',
        unsafe_allow_html=True
    )

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.beta_columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.beta_columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most common words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.beta_columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)



st.sidebar.text("")
st.sidebar.text("")
st.sidebar.markdown("Check the code and working of this app at ([Github](https://github.com/shivamshi))👈")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.markdown("""<a href="https://www.buymeacoffee.com/cvcvcvcvcv"> <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="cvcvcvcvcv" /></a>""")

# CSS styles for the form
st.markdown("""
<style>
    .contact-form {
        text-align: center;
        max-width: 400px;
        margin: 0 auto;
    }
    .input-field {
        width: 100%;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .input-field:focus {
        outline: none;
        border-color: #007BFF;
    }
    .submit-btn {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .submit-btn:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# HTML form with improved UI
st.markdown("""
<h2 style="text-align: center;">Contact me👋</h2>
<form class="contact-form" action="https://formspree.io/f/xwkzngor" method="POST" target="_blank">
    <label for="name">Name</label>
    <input class="input-field" type="text" id="name" name="name" required>
    <br>
    <label for="email">Email</label>
    <input class="input-field" type="email" id="email" name="email" required>
    <br>
    <label for="message">Message</label>
    <textarea class="input-field" id="message" name="message" rows="4" required></textarea>
    <br>
    <button class="submit-btn" type="submit" value="index.html">Send</button>
</form>
""", unsafe_allow_html=True)
