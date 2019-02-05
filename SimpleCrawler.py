import httplib2
import bs4 as bs
from time import sleep
from collections import deque
from urllib.request import urlopen
import collections
from collections import defaultdict

 
 


urls_dfs = []
duplicates_dfs = []

def print_dfs_urls():
    with open('unique-urls-dfs.txt', 'w') as f:
        for item in urls_dfs:
            f.write("%s\n" %  item)
            
def print_dfs_duplicates():
    duplicates_dfs = [item for item, count in collections.Counter(urls_dfs).items() if count > 1]
    with open('duplicates-dfs.txt', 'w') as f:
        for item in duplicates_dfs:
            f.write("%s\n" %  item)

                      
def get_page_links(url):
    urls = []
    http = httplib2.Http()
    sleep(0.1)
    status, response = http.request(url)
    soup = bs.BeautifulSoup(response, "html.parser")
    for div in soup.find_all("div", {"class":"mw-body-content"}):
        for link in div.select("a"):
            if link.has_attr('href'):
                if link['href'].startswith("/wiki/") and link['href'] not in urls_dfs and ":" not in link['href'] and "Main_Page" not in link['href'] and "#" not in link['href']: 
                    urls.append(link['href'])
            
    urls = ['https://en.wikipedia.org' + s for s in urls]
    return urls

#Function which writes the list of duplicate links to a text file
def print_duplicate_links_dfs():
    if len(duplicates_dfs) > 0:
        duplicates_dict = defaultdict(int)
        for d in duplicates_dfs:
             duplicates_dict[d] += 1
        with open('duplicate-links-dfs.txt', 'w') as data:
            data.write(str(duplicates_dict))
            
#Recursive function to crawl in dfs manner
def dfs(url,depth=1):
    links = get_page_links(url) 
    for link in links:
        if len(set(urls_dfs)) < 1001:
             if link in urls_dfs: 
                 duplicates_dfs.append(link)
             if depth < 7 and link not in urls_dfs:    
                 urls_dfs.append(link)
                 dfs(link, depth+1) 
                 


#DFS crawling function      
def dfs_crawl(url):
    dfs(url)
    print_dfs_urls()
    print_duplicate_links_dfs()



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
  
#This list will hold downloaded links
urls_bfs = []    

#This list will hold duplicate links
duplicates_bfs = []
                    
#Function to extract the links from content block of a page and return it in a list
#Checks for conditions such as avoiding administrative	link, links 
#to another section in same page, link to main page, external links	
#Respects politeness policy using a delay before HTTP request
def get_links_bfs(url):
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

#Fubction for BFS crawling                    
def bfs(url):
    queue = deque([(url,0)])
    depth = 1
    while queue and len(set(urls_bfs)) < 1000:
        url,depth = queue.popleft()
        if depth < 7:
                download_page(url)
                if url not in urls_bfs:
                    urls_bfs.append(url)
                links = get_links_bfs(url) 
                for link in links:
                    if link in queue or link in urls_bfs:
                        duplicates_bfs.append(link)
                    if link not in queue and link not in urls_bfs:
                        queue.append((link, depth + 1))
                        
def print_bfs_urls():
    with open('unique-urls-bfs.txt', 'w') as f:
        for item in urls_bfs:
            f.write("%s\n" %  item)
    
def bfs_crawl(url):
    bfs(url)
    print_bfs_urls()
    print_duplicate_links_bfs()


#Function which writes the list of duplicate links to a text file
def print_duplicate_links_bfs():
    if len(duplicates_bfs) > 0:
        duplicates_dict = defaultdict(int)
        for d in duplicates_bfs:
             duplicates_dict[d] += 1
        with open('duplicate-links-bfs.txt', 'w') as data:
            data.write(str(duplicates_dict))

dfs_crawl('https://en.wikipedia.org/wiki/Space_exploration')
bfs_crawl('https://en.wikipedia.org/wiki/Space_exploration')
