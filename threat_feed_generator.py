import feedparser
from datetime import datetime, date, timedelta
from collections import defaultdict
from datetime import datetime 
import time 
import os
import trafilatura
from requests import get
from google import genai

# API key being read from api_config.py file variable set (ensure is included in .gitignore if pushing code via git)
from api_config import GEMINI_API_KEY
## GLOBAL VARIABLES BELOW -- ENSURE CORRECT VALUES ARE SET
####################################
# Default location for text files with links to RSS feeds from sites, keep each URL on a separate line
FEEDS_PATH  = 'rss_feed_links.txt'

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
    # empty list to add feeds to
    feeds = list()
    # process feeds in FEEDS_PATH variable
    with open(FEEDS_PATH, 'r') as feed_file:
        for rss_url in feed_file:
            feeds.append(rss_url.rstrip())
    return feeds

# This function takes the feed links list returned from parse_feed_file()
# It will parse the XML and return links to each individual story
# Will return a dictionary where key is a tuple of (website, article_title, date_published) and value is the list of articles published on that date 
def parse_feeds(feeds) -> dict():
    # dictionary to return all links published on date
    datePublished_articles_dictionary = defaultdict(list)
    # for each feed, read the content into feedparser
    for rss_url in feeds:
        # parse through each individual XML channel for entries
        xml_channel = feedparser.parse(rss_url)
        # individual entry for each article to parse through
        for entry in xml_channel.entries:
            # if feed publish time is in alignment with global variable ranges, then add to dictionary
            local_time_feed_published = time.localtime(time.mktime(entry.updated_parsed))
            entry_date = datetime(*local_time_feed_published[:3]).date()
            if (START_DATE <= entry_date) and (END_DATE >= entry_date):
                datePublished_articles_dictionary[(xml_channel.channel.title, entry.title, entry_date)].append(entry.link.removeprefix("https://"))

    return datePublished_articles_dictionary

# This function will download all the articles passed by a dictionary with the keys as date published and values as article links
# The files will be downloaded into a nested folder called 'articles' with subdirectories being the date the article was published
# and think article links as the file names
def download_articles(parsed_entries: dict):
    # return value of articles dictionary with website name as key and list of articles written to as value (ex: {BleepingComputer} : ['path/to/article', 'path/to/another_article'])
    extracted_articles = defaultdict(list)
    # creates local directory 'articles' to download files into, sorted by date
    for article_data, urls in parsed_entries.items():
        website_name = article_data[0]
        article_name = article_data[1]
        article_date = article_data[2]
        folder_path = f"articles/{website_name}/{article_date}"
        for url in urls:
            # retrieve url content and extract only text from article
            raw_html = trafilatura.fetch_url(url)
            article_content = trafilatura.extract(raw_html)
            os.makedirs(folder_path,exist_ok=True)
            try:
                with open(f"{folder_path}/{article_name}", "w", encoding='utf-8') as f:
                    # make folder & store extracted text to that file named after article title within
                    f.writelines(article_content)
                    extracted_articles[website_name].append(f"{os.getcwd()}/{folder_path}/{article_name}")
                    print(f"Wrote extracted article content to '{os.getcwd()}/{folder_path}/{article_name}' from {website_name}")
            except TypeError:
                os.remove(f"{folder_path}/{article_name}")
                print(url + ' is empty when parsed. Unable to write summary')

    return extracted_articles

def gemini_summarize_articles(article_paths: list):
    return 0

def main():
    feeds = parse_feed_file()
    # take rss feed URLs and go through to extract individual articles/blogs/news links
    # Will return a dictionary where  
    parsed_entries = parse_feeds(feeds) # key is a tuple of (website, article_title, date_published) and value is the list of articles published on that dates
    # Next step step is to create function to download and send article content to LLM for processing
    article_paths = download_articles(parsed_entries)
    # locally download article content that fit in date range from RSS links, return paths in articles folder sorted by date
    print(article_paths)
    # send article content to gemini to summarize
    ##gemini_summarize_articles(article_paths)
    return 0

if __name__ == "__main__":
    main()