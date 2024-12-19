import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from datetime import datetime

def extract_article_data(url, user_date, image_url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example extraction logic; adjust based on site structure
        headline = soup.find('h1').text.strip() if soup.find('h1') else "No headline found"
        body = ' '.join(p.text.strip() for p in soup.find_all('p'))

        # Parse the provided date into the desired format
        try:
            formatted_date = datetime.strptime(user_date, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            formatted_date = "Invalid date format"

        return {
            "Headline": headline,
            "Body": body,
            "Timestamp": formatted_date,
            "Image URL": image_url
        }

    except Exception as e:
        return {"Headline": "Error", "Body": str(e), "Timestamp": "Error", "Image URL": "Error"}

def main():
    st.title("News Article Scraper")
    st.write("Enter three URLs to news articles along with their publication date and image URL to generate a table.")

    urls = []
    user_dates = []
    image_urls = []

    for i in range(3):
        url = st.text_input(f"URL {i+1}", key=f"url_{i+1}")
        user_date = st.text_input(f"Publication Date for URL {i+1} (format: DD/MM/YYYY)", key=f"date_{i+1}")
        image_url = st.text_input(f"Image URL for URL {i+1}", key=f"image_{i+1}")
        if url:
            urls.append(url)
            user_dates.append(user_date)
            image_urls.append(image_url)

    if st.button("Process Articles"):
        if len(urls) < 3:
            st.error("Please provide three URLs before processing.")
        else:
            articles_data = []
            for i, url in enumerate(urls):
                st.write(f"Processing {url}...")
                article_data = extract_article_data(url, user_dates[i], image_urls[i])
                articles_data.append(article_data)

            # Create a table
            df = pd.DataFrame(articles_data)
            st.write("Generated Table:")
            st.dataframe(df)

            # Optionally download the table
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Table as CSV", data=csv, file_name="articles.csv", mime="text/csv")

if __name__ == "__main__":
    main()
