from bs4 import BeautifulSoup
from requests import get
import math

def search(term: str, num_results:int=10, lang: str="en", proxy: str="None", filter_results: bool=True):

    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results(search_term: str , number_results: int, language_code: str, filter_results: bool, start_num: int = 0):
        
        if filter_results==False:
            filter_results=0
        else:
            filter_results=1

        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}&start={}&filter={})'.format(escaped_search_term, number_results+1,
                                                                                       language_code, start_num, filter_results)
        proxies = None
        if proxy:
            if proxy[:5]=="https":
                proxies = {"https":proxy} 
            else:
                proxies = {"http":proxy}
        
        response = get(google_url, headers=usr_agent, proxies=proxies)    
        response.raise_for_status()

        return response.text

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                yield {'url': str(link['href']), 'title': str(title.text)}

    if num_results > 100:
        rounds = math.ceil(num_results/100)
        results = list()
        for i in range(rounds):
            start_num = i*100
            results_temp=list()
            html = fetch_results(term, 100, lang, start_num, filter_results)
            results_temp = list(parse_results(html))
            if len(results_temp) < 100:
                results.extend(results_temp)
                break
            results.extend(results_temp)

    else:
        html = fetch_results(term, num_results, lang, filter_results)
        results = list(parse_results(html))

    return results
