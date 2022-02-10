from bs4 import BeautifulSoup
import requests

class WiktionaryParser():
  @staticmethod
  def fetch_word_details(word):
    url = 'https://el.wiktionary.org/wiki/{}'
    session = requests.Session()
    # session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 1))

    response = session.get(url.format(word))
    if response.status_code == 404:
      return [], [], True

    soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

    compound_words = []
    relative_words = []

    compound_words_header = soup.find(id='Σύνθετα')
    if compound_words_header != None:
      compound_words_list = compound_words_header.find_next('ul')
      for item in compound_words_list.find_all():
        if item.name == 'li':
          compound_words.append(item.text)

    relative_words_header = soup.find(id='Συγγενικές_λέξεις')
    if relative_words_header != None:
      relative_words_list = relative_words_header.find_next('ul')
      for item in relative_words_list.find_all():
        if item.name == 'li':
          relative_words.append(item.text)

    return compound_words, relative_words, False
