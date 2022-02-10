givenSentence = 'Σήμερα πιστεύαμε πως θα ερχόσασταν αλλά τελικά δεν ήταν ευχάριστο το τέλος. Ελπίζω να σου αρέσει το φαγητό'

# --- Stanza ---

import stanza
stanza.download('el')
nlp = stanza.Pipeline('el', processors='tokenize, mwt, pos, lemma')

doc = nlp(givenSentence)

for sentence in doc.sentences:
  for word in sentence.words:
    print(word.text, word.lemma)

print('------------------------------------------------')

# --- spaCy ---
import spacy
nlp = spacy.load('el_core_news_lg')

doc = nlp(givenSentence)

for token in doc:
  print(token, token.lemma_)


# ------------------------------------------------------------------------

# import fasttext
import fasttext.util

fasttext.util.download_model('el', if_exists='ignore')
ft = fasttext.load_model('cc.el.300.bin')
ft.get_dimension()
ft.get_word_vector('νικητής').shape
ft.get_nearest_neighbors('νικητής')

# ------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

class WiktionaryParser(object):
  def __init__(self, word):
    url = 'https://el.wiktionary.org/wiki/{}'
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries = 2))
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries = 2))

    response = session.get(url.format(word))
    soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

    compoundWords = []
    relativeWords = []

    compoundWordsHeader = soup.find(id='Σύνθετα')
    if compoundWordsHeader != None:
      compoundwords_list = compoundWordsHeader.find_next('ul')
      for item in compoundwords_list.find_all():
        if item.name == 'li':
          compoundWords.append(item.text)

    relativeWordsHeader = soup.find(id='Συγγενικές_λέξεις')
    if relativeWordsHeader != None:
      relativewords_list = relativeWordsHeader.find_next('ul')
      for item in relativewords_list.find_all():
        if item.name == 'li':
          relativeWords.append(item.text)
