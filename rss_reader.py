import xml.etree.ElementTree as ET
import requests
import feedparser

def parse_opml(opml_file):
    tree = ET.parse(opml_file)
    root = tree.getroot()
    feeds = []
    
    for outline in root.iter('outline'):
        url = outline.get('xmlUrl')
        if url:
            feeds.append(url)
    return feeds

def fetch_rss(feed_url):
    content = requests.get(feed_url, verify=False).content
    feed = feedparser.parse(content)
    return feed

opml_file = 'output.opml'
feed_urls = parse_opml(opml_file)

for url in feed_urls:
    feed = fetch_rss(url)

    # 檢查 feed 中是否存在 title 屬性
    feed_title = getattr(feed.feed, 'title', 'No Title')
    print(f"Feed Title: {feed_title}")

    for entry in feed.entries:
        entry_title = getattr(entry, 'title', 'No Title')
        entry_link = getattr(entry, 'link', 'No Link')
        entry_published = getattr(entry, 'published', 'No Publication Date')

        print(f"Title: {entry_title}")
        print(f"Link: {entry_link}")
        print(f"Published: {entry_published}")
        print('---')

