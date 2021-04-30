from requests import get
from bs4 import BeautifulSoup
import math


def search(term, num_results=10, lang="en", verbose=False):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results(search_term, number_results, language_code, start_num=0):
        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}&start={}&filter=0'.format(escaped_search_term, number_results+1,
                                                                                       language_code, start_num)
        response = get(google_url, headers=usr_agent)
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
            if verbose:
                print(f"fetching results {start_num} of {num_results}")
            html = fetch_results(term, 100, lang, start_num)
            results_temp = list(parse_results(html))
            if len(results_temp) < 100:
                print(
                    f"only {len(results_temp)} returned, breaking as next page will have no results")
                results.extend(results_temp)
                break
            results.extend(results_temp)

    else:
        html = fetch_results(term, num_results, lang)
        results = list(parse_results(html))

    if verbose:
        print(f"Results: {len(results)}")
    return results
