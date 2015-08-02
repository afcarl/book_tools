import requests
from unidecode import unidecode
import sqlite3
import lxml.html
from subprocess import call
import os

def initialize_database():
    create_schema()
    create_db()
    
def create_schema():
    if os.path.exists("database.db"):
        os.remove("database.db")
    table = """
    drop table if exists html;
    create table html (
    id integer primary key autoincrement,
    url text not null,
    html text not null
    );
    """
    with open("schema.sql","w") as schema:
        schema.write(table)

def create_db():
    call("create_db.sh",shell=True)

def save(url,html):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("insert into html (url,html) values (?,?)",(url,html))
    
class Crawler:
    #6 as a max is recommended for depth
    def __init__(self,base_url,depth,grab_all=False):
        self.base_url = base_url
        #this gets the important parts of the base url
        self.domain_name = self.get_domain_name(base_url)
        self.start_depth = depth
        self.urls = []
        self.num_urls = 0
        self.grab_all = grab_all

    def get_domain_name(self, url):
        return url.split("//")[1].split("/")[0]
    
    def update_base_url(self,base_url):
        self.base_url = base_url

    def update_depth(self,depth):
        self.start_depth = depth

    def links_grab(self,url):
        r = requests.get(url)
        domain_name = self.get_domain_name(url)
        save(url,unidecode(r.text)) #saves to the database, database.db
        html = lxml.html.fromstring(unidecode(r.text))
        url_list = html.xpath("//a/@href") 
        uri_list = []
        for uri in url_list:
            if uri.startswith("/"):
                uri_list.append(domain_name+uri)
            else:
                uri_list.append(uri)
        return uri_list + [url] #ensures the url is stored in the final list

    def crawl(self):
        return self.crawler([self.base_url],self.start_depth)
    
    def crawler(self,urls,depth):
        urls = list(set(urls))
        url_list = []
        for url in urls:
            if self.grab_all:
                url_list += self.links_grab(url)
            else:
                if self.domain_name in url:
                    url_list += self.links_grab(url)
        url_list = list(set(url_list)) #dedup list
        url_list = [uri for uri in url_list if uri.startswith("http")]
        if depth > 1:
            url_list += self.crawler(url_list,depth-1)
        self.urls += url_list
        self.urls = list(set(self.urls))
        self.num_urls = len(self.urls)
        return url_list

if __name__ == '__main__':
    #initialize_database()
    c = Crawler("http://www.backpage.com",2,grab_all=True)
    c.crawl()
    print c.urls
    print c.num_urls
