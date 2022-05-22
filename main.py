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
    print("Membuka file... ")
    with open(self.filename, 'r', encoding="utf-8") as f:
      words = f.read()

      # tokenize words
      tokenization = word_tokenize(re.sub(r"[^a-zA-Z]", " ", words))

      # stem/lemmatize words
      lemmatized_words = self.lemmatizeWords(tokenization)
      
    return lemmatized_words

  def lemmatizeWords(self, tokens):
    print("Proses stemming... ", end="")
    lemm = WordNetLemmatizer()
    pos_tagged = nltk.pos_tag(tokens)
    lemmatized = [lemm.lemmatize(word, tag[0].lower()).lower() if tag[0].lower() in ['a', 'n', 'v'] else lemm.lemmatize(word) for word, tag in pos_tagged]
    print("Berhasil!")
    return list(set(lemmatized))

  def groupByAlphabet(self):
    grouped = {}
    print("\nMengelompokkan berdasarkan alphabet... ", end="")
    for x in string.ascii_lowercase:
      grouped[x] = []
    for word in self.words:
      grouped[word[0].lower()].append(word)
    print("Berhasil!")
    return grouped
  
  def showTable(self):
    grouped = self.groupByAlphabet()
    print("Membuat tabel... ")
    transformed_data = {
      "JUMLAH": [len(x) for x in grouped.values()],
      "DAFTAR KATA": [", ".join(x) if len(x) > 0 else "-" for x in grouped.values()]
    }
    df = pd.DataFrame(transformed_data, index=[x.upper() for x in grouped.keys()])
    print(df)
      
def main():
  print("! Dev by Reinhard Kevin 2019104402")
  menu = 0;
  while menu != 9:
    showMenu()
    try:
      menu = int(input("Pilih menu: "))
    except (ValueError, TypeError):
      print("\nInput harus angka!")
      continue

    if menu == 1:
      try:
        reader = Reader(filename=input("Nama file: "))
      except (FileNotFoundError):
        print("\nFile tidak ditemukan!")
        continue
    elif menu == 2:
      try:
        reader.showTable()
      except (UnboundLocalError):
        print("\nFile belum dibuka!")
        continue
    elif menu == 9:
      print("\nTerima kasih!")

def showMenu():
  print("\n=== Kuis Data Science ===")
  print("1. Buka file")
  print("2. Tampilkan tabel")
  print("9. Keluar")

if __name__ == '__main__':
  main()