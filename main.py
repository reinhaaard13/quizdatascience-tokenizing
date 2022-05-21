import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

class Reader:
  def __init__(self, filename):
    self.filename = filename
    self.words = self.getWords()

  def getWords(self):
    # nltk.download('punkt')
    # nltk.download('omw-1.4')
    # nltk.download('averaged_perceptron_tagger')
    with open(self.filename, 'r', encoding="utf-8") as f:
      words = f.read()

      # tokenize words
      tokenization = word_tokenize(re.sub(r"[^a-zA-Z]", " ", words))

      # stem/lemmatize words
      lemmatized_words = self.lemmatizeWords(tokenization)
      
    return lemmatized_words

  def lemmatizeWords(self, tokens):
    lemm = WordNetLemmatizer()
    pos_tagged = nltk.pos_tag(tokens)
    lemmatized = [lemm.lemmatize(word, tag[0].lower()).lower() if tag[0].lower() in ['a', 'n', 'v'] else lemm.lemmatize(word) for word, tag in pos_tagged]
    return list(set(lemmatized))

  def groupByAlphabet(self):
    grouped = {}
    for x in string.ascii_lowercase:
      grouped[x] = []
    for word in self.words:
      grouped[word[0].lower()].append(word)
    return grouped
  
  def showTable(self):
    grouped = self.groupByAlphabet()
    transformed_data = {
      "JUMLAH": [len(x) for x in grouped.values()],
      "DAFTAR KATA": [", ".join(x) if len(x) > 0 else "-" for x in grouped.values()]
    }
    df = pd.DataFrame(transformed_data, index=[x.upper() for x in grouped.keys()])
    print(df)
      
def main():
  reader = Reader(filename="file.txt")
  reader.showTable()

if __name__ == '__main__':
  main()