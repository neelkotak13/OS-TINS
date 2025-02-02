import feedparser

## GLOBAL VARIABLES BELOW -- ENSURE CORRECT VALUES ARE SET
# Default location for text files with links to RSS feeds from sites, keep each URL on a separate line
FEEDS_PATH  = 'rss_feed_links.txt'
# Location to read API key from, FOR SECURITY REASONS, DO NOT PUBLISH CODE WITH API KEY
GEMINI_API_KEY_PATH = 'llm_api_key.txt'
## END GLOBAL VARIABLES

def parse_feed():
    # empty list to add feeds to
    feeds = list()
    # process feeds in FEEDS_PATH variable
    with open(FEEDS_PATH, 'r') as feed_file:
        for rss_url in feed_file:
            feeds.append(rss_url.rstrip())
    
    # for each feed, read the content into feedparser
    for rss_url in feeds:
        feed = feedparser.parse(rss_url)
    return 0

def main():
    parse_feed()
    return 0

if __name__ == "__main__":
    parse_feed()