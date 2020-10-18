# This is a sample Python script.
import pandas as pd
import simplejson as json
# import spacy
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
# from rank_bm25 import BM25Okapi
# from tqdm import tqdm
# nlp = spacy.load("en_core_web_sm")
pd.set_option('display.max_colwidth', None)

# data_file = open("all_data.json", "r", encoding="utf8")
#
# json_data = json.load(data_file, encoding="utf8")
#
# print(json_data)

df_all_data = pd.read_json("all_data.json", orient="records", encoding="utf8")

print(df_all_data.columns)

documents = []

for i in range(len(df_all_data)):
    documents.append(df_all_data.loc[i, "name"] + " " + str(df_all_data.loc[i, "description"]) + " " + df_all_data.loc[i, "categories"].replace("/", " ") + " " + str(df_all_data.loc[i, "brand"]))

print("Doc length:", len(documents))

word_counts = defaultdict(int)
for document in documents:
    for word in document.lower().split(" "):
        word_counts[word] += 1

for key, value in word_counts.items():
    if value > 10000:
        print(key, value)

stoplist = ["with", "for", "home", "page", "&", "nan", "of", "-", "a", "to", "the", ""]

texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)


from flask import Flask

app = Flask("walmart-flask")

@app.route('/')
def home():
    return "Hello World"

@app.route('/<query>')
def make_query(query):
    doc = query
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    # print(vec_lsi)

    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('tmp\\iphonecase.index')
    index = similarities.MatrixSimilarity.load('tmp\\iphonecase.index')

    sims = index[vec_lsi]  # perform a similarity query against the corpus
    # print(list(enumerate(sims)))  # print (document_number, document_similarity) 2-tuples

    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:50]
    products = []
    for i, s in enumerate(sims):
        products.append({"url":df_all_data.loc[i, "url"],"name":df_all_data.loc[i, "name"],"category":df_all_data.loc[i, "categories"],"relevance":str(s)})
        print(s, documents[i])

    return json.dumps(products, ensure_ascii=False)

if __name__ == '__main__':
    app.run()

# text_list = df.description.str.lower().values
# tok_text=[] # for our tokenised corpus
# #Tokenising using SpaCy:
# for doc in tqdm(nlp.pipe(text_list, disable=["tagger", "parser","ner"])):
#    tok = [t.text for t in doc if t.is_alpha]
#    tok_text.append(tok)
#
# bm25 = BM25Okapi(tok_text)
#
# query = "Flood Defence"
# tokenized_query = query.lower().split(" ")
# import time
# t0 = time.time()
# results = bm25.get_top_n(tokenized_query, df.text.values, n=3)
# t1 = time.time()
# print(f'Searched 50,000 records in {round(t1-t0,3) } seconds \n')
# for i in results:
#    print(i)