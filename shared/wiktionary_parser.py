from bs4 import BeautifulSoup
import requests

def fetch_word_details(word):
  if not active_internet_connection_exists(): raise RuntimeError
  url = 'https://el.wiktionary.org/wiki/{}'
  session = requests.Session()
  # session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
  session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 1))

  response = session.get(url.format(word))
  if response.status_code == 404:
    return [], True

  soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

  family_words = set()

  compound_words_header = soup.find(id='Σύνθετα')
  if compound_words_header != None:
    compound_words_list = compound_words_header.find_next('ul')
    for item in compound_words_list.find_all():
      if item_is_valid(item):
        family_words.add(clean_word(item.text))

  relative_words_header = soup.find(id='Συγγενικές_λέξεις')
  if relative_words_header != None:
    relative_words_list = relative_words_header.find_next('ul')
    for item in relative_words_list.find_all():
      if item_is_valid(item):
        family_words.add(clean_word(item.text))

  return list(family_words), False

def active_internet_connection_exists():
  try:
    requests.get(url = "https://www.google.com", timeout = 1)
  except (requests.ConnectionError, requests.Timeout) as exception:
    return False

  return True

def item_is_valid(item):
  if item.name != 'li':
    return False

  forbidden_substrings = ['δείτε', '-']
  for substring in forbidden_substrings:
    if substring in item.text:
      return False

  return True

def clean_word(word):
  forbidden_characters = [',', '(', ' και']
  for character in forbidden_characters:
    new_word = word.split(character)[0]
    if character == '(' and not new_word:
      new_word = word.split(')')[1]

    word = new_word

  return word.strip()
