import feedparser
import psycopg2
from datetime import datetime
import time

# PostgreSQL config

DB_CONFIG = {
   'host': 'aws-0-ca-central-1.pooler.supabase.com',
    'port': '5432',
    'dbname': 'postgres',
    'user': 'postgres.ukepmwoqxybhauovasry',
    'password': 'FinAnswer@Loyalist'
    }
#--}    

#--DB_CONFIG = {
   #-- 'host': 'localhost',
    #--'port': '5432',
    #--'dbname': 'finQA',
    #--'user': 'postgres',
    #--'password': 'mypostgres'
#--}

def get_news_from_rss(stock_symbol):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={stock_symbol}&region=US&lang=en-US"
    print(f"📡 Fetching RSS feed from: {url}")
    
    feed = feedparser.parse(url)
    news_data = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published = entry.published  # 'Thu, 05 Jun 2025 13:45:00 +0000'
        timestamp = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
        image_url = None  # RSS feed doesn't include images

        news_data.append((stock_symbol, title, link, image_url, timestamp))

    print(f"📰 Found {len(news_data)} articles for {stock_symbol}")
    return news_data

def store_in_db(news_items):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print(f"📥 Inserting {len(news_items)} articles into DB...")
        for item in news_items:
            cur.execute("""
                INSERT INTO yahoo_news (stock_symbol, title, url, image_url, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, item)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ DB insert complete.")
    except Exception as e:
        print(f"❌ DB Insert Error: {e}")

def main():
    symbols = ['AAPL', 'TSLA', 'GOOG', 'AMZN']
    for symbol in symbols:
        print(f"\n=============================")
        print(f"🔄 Scraping news for {symbol}")
        news = get_news_from_rss(symbol)
        store_in_db(news)
        time.sleep(2)  # polite delay

if __name__ == '__main__':
    main()
