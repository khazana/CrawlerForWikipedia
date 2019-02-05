from urllib.request import urlopen
import bs4 as bs
from nltk import stem, tokenize
from nltk.corpus import wordnet
import httplib2
from time import sleep
from collections import deque
from collections import defaultdict


#Stemmer object for text cleaning
stemmer = stem.PorterStemmer()

#List of downloaded webpages
downloads = [] 

#List of duplicate links
duplicates = []  

#threshold to decide whether a page is relavant or not
threshold = 5

#convert the string into lowercase and do stemming
def clean_text(content):
    lowercase_content = tokenize.wordpunct_tokenize(content.lower().strip())
    return ' '.join([stemmer.stem(word) for word in lowercase_content])

#find synonyms of the keyword so that they can also be searched for occurrences
#also finds synonyms of the words in a phrase
def find_synonyms(keyword):
    synonyms = []
    keyword_list = keyword.split()
    for i in range(0,len( keyword_list)):
        for synonym in wordnet.synsets(keyword_list[i]): 
            for l in synonym.lemmas(): 
                synonyms.append(l.name())  
    return list(synonyms)


#download the page and save it using the name '/wiki/...'
#this will help us construct URLS if required in future
def download_page(url):
    page = urlopen(url)
    html_content = page.read()
    html_content = str(html_content)
    url = url.split('https://en.wikipedia.org/',1)[1].replace("/","-")
    file = open(url + '.txt', 'w')
    file.write(html_content)
    file.close()
 

#Boolean function used to check if a page is relavant enough to be downloaded 
#The page should only be downloaded if the following conditions are satisfied:
#1.The keyword appears at least five times in the article
#2.A single variation of the keyword appears at least five times in the article
#3.Multiple variations of the keyword appear together at least five times in the article
def should_page_be_downloaded(link, keyword):
    if link not in downloads:
        keyword = clean_text(keyword)
        other_keywords= find_synonyms(keyword)
        soup = bs.BeautifulSoup(urlopen(link),features="lxml")
        content = soup.find("div", {"class":"mw-content-ltr"}).text
        new_content = clean_text(content)
        keyword = stemmer.stem(keyword.lower())
        if new_content.count(keyword) > threshold :
            return True
        else:
            if len(other_keywords) > 0:
                variations_count = 0
                for x in other_keywords:
                    variations_count = variations_count +  new_content.count(x) 
                    if variations_count > threshold:
                        return True
    return False
    
#Function to extract the links from content block of a page and return it in a list
#Checks for conditions such as avoiding administrative	link, links 
#to another section in same page, link to main page, external links	
#Respects politeness policy using a delay before HTTP request
def get_links(url):
    urls = []
    http = httplib2.Http()
    sleep(0.1)
    status, response = http.request(url)
    soup = bs.BeautifulSoup(response, "html.parser")
    for div in soup.find_all("div", {"class":"mw-body-content"}):
        for link in div.select("a"):
            if link.has_attr('href'):
                if link['href'].startswith("/wiki/") and ":" not in link['href'] and "Main_Page" not in link['href'] and "#" not in link['href']: 
                    urls.append(link['href'])
    urls = ['https://en.wikipedia.org' + s for s in urls]
    return urls


#Function which writes the list of duplicate links to a text file
def print_duplicate_links():
    if len(duplicates) > 0:
        duplicates_dict = defaultdict(int)
        for d in duplicates:
             duplicates_dict[d] += 1
        with open('duplicate_links.txt', 'w') as data:
            data.write(str(duplicates_dict))
        
#Function which writes the list of downloaded links to a text file
def print_downloaded_links():
        with open('downloaded_links.txt', 'w') as f:
            for item in downloads:
                f.write("%s\n" %  item)

#Function which performs BFS crawling 
#Crawls until required number of unique URLS is reached
#Does not add duplicate links to queue
def bfs_crawl(url,keyword):
    queue = deque([(url,0)])
    depth = 1
    while queue and len(set(downloads)) < 1001:
        url,depth = queue.popleft()
        if depth < 7:
            if should_page_be_downloaded(url,keyword):
                download_page(url)
                downloads.append(url)
                links = get_links(url) 
                for link in links:
                    if link in queue or link in downloads:
                        duplicates.append(link)
                    if link not in queue and link not in downloads:
                        queue.append((link, depth + 1))
            
                    
#main function to do focused crawling    
def focused_crawl(url,keyword):
    bfs_crawl(url, keyword)
    print_duplicate_links()
    print_downloaded_links()


focused_crawl('https://en.wikipedia.org/wiki/Computer', "computer")
