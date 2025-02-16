import feedparser
from datetime import datetime, date, timedelta
from collections import defaultdict
from datetime import datetime 
import time 

## GLOBAL VARIABLES BELOW -- ENSURE CORRECT VALUES ARE SET
####################################
# Default location for text files with links to RSS feeds from sites, keep each URL on a separate line
FEEDS_PATH  = 'rss_feed_links.txt'

# Location to read API key from, FOR SECURITY REASONS, DO NOT PUBLISH CODE WITH API KEY
GEMINI_API_KEY_PATH = 'llm_api_key.txt'

# Start date of articles to start parsing (note sites may only post dates in a limited range of times)
#yesterday = time.time() - 2*86400 # subtracting 48 hours worth of seconds to get day before yesterday 
#START_DATE = time.struct_time(time.localtime(yesterday))

#yesterday = 
#dt_yesterday = datetime(int(time.localtime(*yesterday[:6])))
START_DATE = date.today() - timedelta(days=2)

# End date of articles to complete parsing (set to same day as start date if only for a single day)
END_DATE = date.today()

####################################
## END GLOBAL VARIABLES

# This function will parse the FEEDS_PATH designated file reading each line as a separate URL for RSS feeds
# By default this will contain the sites bleepingcomputer, darkreading, and krebsonsecurity rss links
def parse_feed_file() -> list:
    print(START_DATE)
    print(END_DATE)
    # empty list to add feeds to
    feeds = list()
    # process feeds in FEEDS_PATH variable
    with open(FEEDS_PATH, 'r') as feed_file:
        for rss_url in feed_file:
            feeds.append(rss_url.rstrip())
    return feeds

# This function takes the feed links list returned from parse_feed_file()
# It will parse the XML and return links to each individual story
# Will return a dictionary where key is the published date and value is the list of articles published on that date 
def parse_feeds(feeds) -> dict():
    # dictionary to return all links published on date
    datePublished_articles_dictionary = defaultdict(list)
    print(datePublished_articles_dictionary)
    # for each feed, read the content into feedparser
    for rss_url in feeds:
        # parse through each individual XML channel for entries
        channel = feedparser.parse(rss_url)
        # individual entry for each article to parse through
        for entry in channel.entries:
            # if feed publish time is in alignment with global variable ranges, then add to dictionary
            local_time_feed_published = time.localtime(time.mktime(entry.updated_parsed))
            entry_date = datetime(*local_time_feed_published[:3]).date()
            if (START_DATE <= entry_date) and (END_DATE >= entry_date):
                datePublished_articles_dictionary[entry_date].append(entry.link)

    return datePublished_articles_dictionary

def main():
    feeds = parse_feed_file()
    # take rss feed URLs and go through to extract individual articles/blogs/news links
    parsed_entries = parse_feeds(feeds) # returns dictionary where key is articles published date and value is a list of article links
    # Next step step is to create function to download and send article content to LLM for processing
    return 0

if __name__ == "__main__":
    main()