from bs4 import BeautifulSoup
from requests import get
import math

def search(term: str, num_results:int=10, lang: str="en", proxy: str="None", filter_results: bool=True):

    verbose=False

    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results(search_term: str , number_results: int, language_code: str, filter_results: bool, start_num: int = 0):
        
        if filter_results==False:
            filter_results:int=0
        else:
            filter_results:int=1

        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}&start={}&filter={})'.format(escaped_search_term, number_results,
                                                                                       language_code, start_num, filter_results)
        proxies = None
        if proxy:
            if proxy[:5]=="https":
                proxies = {"https":proxy} 
            else:
                proxies = {"http":proxy}
        
        response = get(google_url, headers=usr_agent, proxies=proxies)

        if verbose:
            print(f"[fetch_results] Search URL: {google_url}")
            print(f"[fetch_results] Proxy: {proxies})")

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

    search_step=50
    rounds = math.ceil(num_results/search_step)

    #Google often returns 2 or so items less than requested. Oversearch and then trim the results.
    search_total=num_results+(2*rounds)

    results = list()
    for i in range(rounds):

        start_num = i*search_step
        if (search_step*(i+1))>search_total:
            step=search_total-(i*search_step)
        else:
            step=search_step

        if verbose:
            print(f"Round:{i}, rounds: {rounds} ")
            print(f"start_num:{start_num}, step:{step}")
        
        results_temp=list()
        html = fetch_results(term, step, lang, filter_results, start_num)
        results_temp = list(parse_results(html))

        if verbose:
            print(f"Step Results:{len(results_temp)}")

        if len(results_temp) < step-2:
            # recieved less results than requested, search exausted.
            results.extend(results_temp)
            break
        results.extend(results_temp)
    
    if len(results)>num_results:
        results=results[:num_results]
    if verbose:
        print(f"Total results len:{len(results)}")
    return results
