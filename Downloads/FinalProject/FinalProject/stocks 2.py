import pandas as pd

import datetime

from datetime import datetime

from datetime import timedelta

from operator import itemgetter

import requests

import re

import csv

from requests import get

from requests.exceptions import RequestException

from contextlib import closing

from bs4 import BeautifulSoup

import urllib

import unittest

from collections import defaultdict, OrderedDict, Counter

import string


def get_content(url):
    """

    Attempts to get the content at `url` by making an HTTP GET request.

    If the content-type of response is some kind of HTML/XML, return the

    text content, otherwise return None

    from https://realpython.com/blog/python/python-web-scraping-practical-introduction/

    """

    try:

        with closing(get(url, stream=True)) as resp:

            if is_good_response(resp):

                return resp.content

            else:

                return None

    except RequestException as e:

        log_error('Error during requests to {0} : {1}'.format(url, str(e)))

        return None


def is_good_response(resp):
    '''

    Returns true if the response seems to be HTML, false otherwise

        From https://realpython.com/blog/python/python-web-scraping-practical-introduction/

        '''

    content_type = resp.headers['Content-Type'].lower()

    return (resp.status_code == 200

            and content_type is not None

            and content_type.find('html') > -1)


def log_error(e):
    '''

    Print errors

    from https://realpython.com/blog/python/python-web-scraping-practical-introduction/

    '''

    print(e)


def findTopOccurrences(url):

    try:
    	with closing(get(url, stream=True)) as resp:

            if is_good_response(resp):

                d = defaultdict(int)

                raw_html = (urllib.request.urlopen(url)).read()

                parsable = BeautifulSoup(raw_html, 'html.parser')

                # Split url text into lowercase words

                word_list = parsable.get_text().lower().split()

                for i in word_list:

                    d[i] += 1

                return OrderedDict(sorted(d.items(), key=itemgetter(1)))

    except RequestException as e:

        print("error")

        log_error('Error during requests to {0} : {1}'.format(url, str(e)))

        return None


def populate(x):

    # Create dictionary mapping all words to all Occurrences

    tick = open(x, 'r')

    rows = tick.read().split('\n')

    urls = list()

    for i in rows:

        x = i.split(',')

        urls.append(x[1])

    d = dict()

    for site in urls:

        d = Counter(d) + Counter(findTopOccurrences(site))

    return d


def clean():

    # Cleaning:

    # We will begin by removing all entries that are in the negative key words
    # - so we can isolate which keywords ONLY pertain to positive announcements

    print("BEGIN CLEANING")
    print("Training positive announcement data")
    pos = populate('tickers_training.csv')
    print("Training negative announcement data")
    neg = populate('tickers_neg_training.csv')

    print("Isolating which keywords ONLY pertain to positive announcements")
    for i in neg.keys():

        if i in pos.keys():

            pos.pop(i)


    # Next, to reduce clutter, we will delete all words that only appear less
    # than four times.
    print("Deleting all words that only appear less than four times")
    pos = {k: v for k, v in pos.items() if v >= 4}

    # Next, we will proceed by removing all entries that have special
    # characters in them.
    print("Removing all entries with special characters")
    special_characters = ['!', '#', '$' '%', '&', '(', ')', '*', '+', '.', '/', ':', ';', '<',

                          '=', ',', '>', '?', '@', '[', '\\', ']', '^', '_', '\'', '{', '|', '}', '~', '1', '2', '3', '4',

                          '5', '6', '7', '8', '9', '0', '®']

    keys = list(pos.keys())

    for c in special_characters:

        for word in keys:

            if c in word:

                if word in pos:

                    pos.pop(word)


    # We have to do "-" as a special case because it is often contained in
    # important keywords

    if '–' in pos.keys():

        pos.pop('–')

    print("Removing all entries that are common words according to Wikipedia")

    # Next, we will proceed by removing all entries that are common words
    # according to Wikipedia

    # and all entries that are a single character

    # Source: en.wikipedia.org/wiki/Most_common_words_in_English

    alpha = list(string.ascii_lowercase)

    common = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'on', 'with', 'he',

              'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or',

              'an', 'will', 'my', 'would', 'there', 'their', 'what', 'so', 'up', 'if', 'about', 'who', 'which', 'go', 'me', 'when', 'can', 'like', 'though']

    full = common + alpha

    # Next, we will remove all entries corresponding to a specific disease,
    # certain drug

    # or a certain company to generalize the list to terms that can be applied
    # to any article.

    companies = ['reuters', 'nasdaq', 'apricus', 'abattis', 'bioceuticals', 'biosciences', 'gabriola', 'aclaris', 'adamis',

                 'pharmaceuticals', 'pharmacokinetics', 'easl', 'aerpio', 'therapeutics', 'antibe', 'corporation', 'corp', 'inc', 'citagenix',

                 'aradigm', 'assembly', 'biosciences', 'asmb', 'axsome', 'aytu', 'bioscience', 'company', "company’s", 'khouri', 'thomson']

    diseases = ['scleroderma', "raynaud's", 'phenomenon', 'multiple', 'seborrheic', 'keratosis', 'sk', 'skin', 'tumor', 'lesions',

                'kertoses', 'asthma', 'carcinogenicity', 'obstructive', 'pulmonary', 'cancer', 'blood', 'disease', 'diabetic', 'macular', 'edema', 'dme', 'cst',

                'gastrointestinal', 'non-cystic', 'fibrosis', 'cystic', 'bronchiectasis', 'aeruginosa', 'hbv', 'hepatitis', 'hbeag', "Alzheimer's",

                'retinopathy', 'ulceration', 'viral', 'central', 'nervous', 'cns', 'vascular']

    drugs = ['rayva', 'vitaros', 'cannanumus', 'apc', 'salmeterol', 'xinafoate', 'inhalations', 'akb', 'lucentis', 'atb', 'pulmaquin',

             'biotherapeutics', 'axs', 'esbupropion', 'dextromethorphan', 'device', 'devices' 'enantiomer', 's-enantiomer', 'enantiomers', 'bupropion', 'natesto', 'cannabis', 'antiviral',

             'nicotinic', 'cryotherapy', 'inhaler', 'inhalation', 'acetylcholine', 'norepinephrine']

    specifics = companies + diseases + drugs

    print("Removing all words partaining to specific companies, diseases, or drugs")

    # Finally, we will remove all entries corresponding to website related
    # Occurrences such as advertisements, dropdowns, html commands,

    # embedded posts, and page dimensions. Source:
    # https://www.w3schools.com/html/default.asp

    html = ['html', 'add', 'rawheadline', 'meta', 'powder', 'profile', 'carousel', 'suggestedquality', 'len', 'newlen', 'maxlen', 'newstr', 'smartwidth', 'smartlength',

            'smartheight', 'smartmedia', 'blockquote', 'pullquote', 'hastouch', 'download', 'upload', 'p', 'pe', 'click', 'clicks', 'hover', 'toggle', 'button', 'poster', 'image',

            'cookie', 'cookies', 'player', 'playbackquality', 'sponsored', 'twitterapiurl', 'facebookapiurl', 'page-rank', 'log-rank', 'link', 'links', 'hack', 'user',

            'object', 'sizing', 'modal', 'san', 'visual', 'effects']

    # Now we will combine the common words list, alphabet list, companies
    # list, diseases list, drugs list, and website related Occurrences list

    cleanup = full + specifics + html
    print("Removing all words pertaining to html commands")
    for i in cleanup:

        if i in pos.keys():

            pos.pop(i)

    return pos

    


def testStocks():

    # Import tickers and corresponding urls, start dates, and start times

    

    tickers = open('tickers.csv', 'r')

    rows = tickers.read().split('\n')
    ticker_list = []
    url_list = []
    start_date_list = []
    start_time_list = []
    result_list = []

    for x in rows:
        l = x.split(',')
        ticker_list.append(l[0].strip('ï»¿'))
        url_list.append(l[1])
        start_date_list.append(l[2])
        start_time_list.append(l[3])
        result_list.append(int(l[4]))
    #Create dictionary of common positive keywords
    positive = clean()
    p = positive.keys()
    #Create new lists for the tickers, start times, and start dates of the positive ones
    ticker_list_FINAL = []
    start_time_list_FINAL = []
    start_date_list_FINAL = []
    correct = 0
    print("Checking test data trial announcements for positive keywords")
    for url in url_list:
        #Create a dictionary of all the Occurrences of every word in the url link
        d = findTopOccurrences(url)
        dk = d.keys()
        for c, v in enumerate(p):
            if v in dk:
                #If a known positive keyword appears at least 4 times in the article, then it is marked as positive
                if d[v] >= 4:
                    if ticker_list[c] not in ticker_list_FINAL:
                        ticker_list_FINAL.append(ticker_list[c])
                        start_date_list_FINAL.append(start_date_list[c])
                        start_time_list_FINAL.append(start_time_list[c])
                        correct += result_list[c]
                        break

    print("Stocks bought:", ticker_list_FINAL)

    getStockPeaks(ticker_list_FINAL, start_date_list_FINAL, start_time_list_FINAL)

    precision = correct / len(ticker_list_FINAL)

    print("Precision:", precision * 100, "%")


def getStockPeaks(ticker_list_FINAL, start_date_list_FINAL, start_time_list_FINAL):

    maxes = []

    sum_deltas = 0

    for i, x in enumerate(ticker_list_FINAL):

        start_date = datetime.strptime(
            start_date_list_FINAL[i] + " " + start_time_list_FINAL[i], '%m/%d/%Y %H:%M')

        info = get_google_finance_intraday(x, start_date)['Close']

        price_list = info.values.tolist()

        max_price = max(price_list)

        seconds = price_list.index(max_price)

        maxes.append(seconds)

        avg_time = round(sum(maxes) / len(maxes))

        try:
        	price_delta = (price_list[avg_time] - price_list[0])/price_list[0] * 100
        	
        	sum_deltas += price_delta
        
        except:
        	
        	continue

    print("Average time to sell stocks:", avg_time, "s after trial announcement publication")

    print("MONEY MADE:", sum_deltas, "from", len(ticker_list_FINAL), "stocks")


def get_google_finance_intraday(ticker, start, period=60, days=2):
    """

    Retrieve intraday stock data from Google Finance.

    Parameters

    ----------

    ticker : str

        Company ticker symbol.

    period : int

        Interval between stock values in seconds.

    days : int

        Number of days of data to retrieve.

    Returns

    -------

    df : pandas.DataFrame

        DataFrame containing the opening price, high price, low price,

        closing price, and volume. The index contains the times associated with

        the retrieved price values.



    SOURCE: https://gist.github.com/lebedov/f09030b865c4cb142af1

    **EDITED SOURCE CODE**

    """

    uri = 'http://www.google.com/finance/getprices' \
        '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,

                                                                        period=period,

                                                                        days=days)

    page = requests.get(uri)

    reader = csv.reader(page.content.decode("utf-8").splitlines())

    columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    rows = []

    times = []

    for row in reader:

        if re.match('^[a\d]', row[0]):

            if row[0].startswith('a'):

                times.append(start)

            elif row[0] == start + timedelta(days=1):

                break

            else:

                times.append(start + timedelta(seconds=period * int(row[0])))

            rows.append(map(float, row[1:]))

    if len(rows):

        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),

                            columns=columns)

    else:

        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))


def main():

    testStocks()


if __name__ == "__main__":

    """ Runs main() if we run this file with 'python3 hw1.py'. """

    main()
