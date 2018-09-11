# bio-stock-picker

Niyathi Chakrapani
Anshuman Konuru

Modules used:
Datetime - used in getStockPeaks(), get_google_finance_intraday(), to format and use datetime information for pharma trial 
announcement publications, e.g. line 346
Pandas - used in get_google_finance_intraday() to make dataframes to handle information, e.g. 453
Requests - used in get_content, get_google_finance_intraday() for webscraping, e.g. 423
Re - used in get_google_finance_intraday() for matching, 435
csv - used in get_google_finance_intraday() to read and parse data, 425
RequestException - used in get_content() to handle and log errors during webscraping, 55
closing - used in get_content(), findTopOccurrences() during webscraping, 95
BeautifulSoup - used in findTopOccurrences() to parse html data, 103
urllib - used in findTopOccurrences() to read html, 101
Used for data structures:
defaultdict - used in findTopOccurrences(), 99
OrderedDict - used in findTopOccurences(), 113
Counter - used in findTopOccurences(), 144
string - used in clean(), 213

Classes from top to bottom:
get_content(), is_good_response() and log_error() work in conjunction to get the content at a url by making an HTTP request.
is_good_response() and log_error() specifically test whether the response is an HTML and print errors, respectively.
findTopOccurrences() creates a dictionary mapping all words in a url to their occurrences.
populate() calls findTopOccurrences() to apply it to many urls.
clean() calls populate() to get this dictionary, then "cleans" or removes entries that have irrelevant words or special 
characters.
testStocks() gets a csv with information on stock tickers, urls for their trial announcements, the date and time of
those announcements, and whether the announcements are positive or negative. It parses this info, cleans (calls clean()) it,
and reduces the inputted info to just very positive stocks and their urls, dates and times. It then calculates the precision
and calls getStockPeaks()
getStockPeaks() finds, for all the positive trial announcement tickers from testStocks(), the average time that the stock
peak occurs. It then calculates how much money you would make from buying all these stocks and selling it at that time.

No generators/decorators were used.

Brief Synopsis:
We used training and testing ML to identify what keywords correspond to positive pharmaceutical trial announcements. 
Then, after cleaning the dictionary of these keywords, we were able to use them to identify which pharmaceutical trial 
announcements were outstandingly positive in our test data set (were very strongly positive) From there, we tested 
the precision of our positive labels against manually-determined announcement results (instead of recall, we wanted 
to ensure that all announcements that we labeled positive, were indeed positive). We found the average time of stock peak 
after the announcement within the same day, then calculated the amount of money that would be made by buying the
stocks at the announcement time and selling them at this calculated average time. Combining the results from multiple runs,
this number is overwhelmingly positive.

To launch the project, simply build/run it and you will see the step outputs, as well as the final output of how much
money you made!

Feel free to use this code for personal use. For commercial use please contact niyathic.
