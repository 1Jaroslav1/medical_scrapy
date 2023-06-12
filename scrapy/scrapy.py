import bs4 as bs
from urllib import request
from urllib.request import Request, urlopen


class Scrapy:
    @staticmethod
    def get_subpage_soup(url_base, sub_href):
        try:
            requests_site = Request(url_base + sub_href, headers={"User-Agent": "Mozilla/5.0"})
            source = urlopen(requests_site).read()
            soup = bs.BeautifulSoup(source, 'lxml')
            return soup
        except Exception as e:
            print(e)
            return None

