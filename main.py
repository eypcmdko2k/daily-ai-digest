import feedparser
import datetime
from openai import OpenAI

# Configuration
RSS_FEEDS = [
    "https://hnrss.org/newest?q=AI",
    "https://www.reddit.com/r/artificial/.rss",
]
MAX_ITEMS = 5

def fetch_news():
    items = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:MAX_ITEMS]:
            items.append(entry.title)
    return items

def summarize_with_llm(news_titles):
    client = OpenAI()  # set OPENAI_API_KEY env
    prompt = f"Today is {datetime.date.today()}. Summarize these AI news in 3 bullet points: \n" + "\n".join(news_titles)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

def generate_daily_digest():
    print("Fetching news...")
    titles = fetch_news()
    if not titles:
        print("No news found.")
        return
    print(f"Collected {len(titles)} headlines.")
    print("Summarizing with LLM...")
    summary = summarize_with_llm(titles)
    print("\n--- Daily AI Digest ---")
    print(summary)

if __name__ == "__main__":
    generate_daily_digest()
