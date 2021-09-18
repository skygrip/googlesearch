# googlesearch
googlesearch is a Python library for searching Google, easily. googlesearch uses requests and BeautifulSoup4 to scrape Google.

Fork of /Nv7-GitHub/googlesearch to add addional features such as searching for more than 100 results 

## usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
from googlesearch import search
search("Google")
```
## Additional options
googlesearch supports a few additional options. By default, googlesearch returns 10 results, and similar search results filtered out, you can change that.
```python
from googlesearch import search
search("Google", num_results=140, filter_results=False)
```
In addition, you can change the language google searches in. For example, to get results in French run the following program:
```python
from googlesearch import search
search("Google", lang="fr")
```
## googlesearch.search
```python
googlesearch.search(str: term, int: num_results=10, str: lang="en", bool: filter_results=True) -> list
```