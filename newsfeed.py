from newspaper import Article
from newsapi.newsapi_client import NewsApiClient
import re


def get_newsurls(limit=5, query=None):
    """Returns list of news urls from newsapi.org."""

    # initialise newsapi
    KEY = 'key'  # insert your newsapi key
    newsapi = NewsApiClient(api_key=KEY)

    results = list()
    if query is None:  # get top headlines for Singapore news
        top_headlines_results = newsapi.get_top_headlines(language='en', country='sg')
        results.extend(top_headlines_results['articles'][:limit])

    else:  # get search results from a query
        search_results = newsapi.get_everything(q=query, language='en',
                                                domains='channelnewsasia.com, todayonline.com, straitstimes.com')
        results.extend(search_results['articles'][:limit])

    urls = [article['url'] for article in results]

    return urls

def get_newsfeed():
    """Returns list of scraped news articles."""

    urls = get_newsurls()
    newsfeed = list()
    for num, url in enumerate(urls, start=1):
        article = Article(url)
        article.download()
        article.parse()
        title = str(article.title)

        newsfeed.append(
            (num, url, title)
        )

    return newsfeed

def get_searchfeed(query):
    """Return search results from search query."""

    urls = get_newsurls(query=query)

    if urls is not None:
        searchfeed = list()
        for num, url in enumerate(urls, start=1):
            article = Article(url)
            article.download()
            article.parse()
            title = str(article.title)

            searchfeed.append(
                (num, url, title)
            )

        return searchfeed

    else: return None


def summarise(url):
    """Summarise a news article."""

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    return cleanup(article.summary)


def cleanup(text):
    """Removes unwanted words from text."""

    junk = re.compile("(AdvertisementAdvertisement)|(.*\(Photo:.*\))")

    return junk.sub('', text)
