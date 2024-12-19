import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def extract_article_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example extraction logic; adjust based on site structure
        headline = soup.find('h1').text.strip() if soup.find('h1') else "No headline found"
        body = ' '.join(p.text.strip() for p in soup.find_all('p'))
        publication_date = soup.find('time').text.strip() if soup.find('time') else "No date found"

        return {
            "Headline": headline,
            "Body": body,
            "Publication Date": publication_date
        }

    except Exception as e:
        return {"Headline": "Error", "Body": str(e), "Publication Date": "Error"}

def main():
    st.title("News Article Scraper")
    st.write("Enter three URLs to news articles to generate a table with Headline, Body, and Publication Date.")

    urls = []
    for i in range(3):
        url = st.text_input(f"URL {i+1}", key=f"url_{i+1}")
        if url:
            urls.append(url)

    if st.button("Process Articles"):
        if len(urls) < 3:
            st.error("Please provide three URLs before processing.")
        else:
            articles_data = []
            for url in urls:
                st.write(f"Processing {url}...")
                article_data = extract_article_data(url)
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
