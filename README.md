# Crawler For Wikipedia
Code to crawl Wikipedia using BFS and DFS

This projects consists of two python files - one consists of code for the implementation of a crawler using breadth first search and depth first search. The other file FocusedCrawler.py consists of the code or the implementation of a focused crawler. The SimpleCrawler.py returns four text files - two for a list of unique URLS fetched using BFS and DFS; and another two files consisting of duplicate URLS retrieved using BFS and DFS. The focused crawler also gives a text file for unique URLs as well as one for duplicate URLs.

## Libraries used
URLLIB, NLTK, Beautiful soup, httplib2, time, collections

## Installation
 
This project requires Python 2.7. There are a few packages which have to be installed to be able to run the code. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them as follows:


```bash
pip install foobar
pip install urllib
pip install bs4 
pip install nltk
pip install httplib2
pip install time
pip install collections
```

## Usage

```bash
python SimpleCrawler.py
python FocusedCrawler.py
```

