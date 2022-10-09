from flask import Flask, jsonify, request

from contracts_pb2 import ModelServiceAnswer

import psycopg2
import logging
import pickle
from scipy.spatial import distance
from sklearn.cluster import KMeans

import pandas as pd
import nltk
import numpy as np
import re
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from scipy.spatial import distance
nltk.download('punkt')   # one time execution
nltk.download('stopwords')  # one time execution
from nltk.corpus import stopwords
# 
#sentence tokenization

from nltk.tokenize import sent_tokenize
  
app = Flask(__name__)


def summarize(article, n_sentences=3):
    """
        input:
            string  article: full article, with or without preprocessing, 
                             better without title
            int     n_sentences: number of sentences in summary

        output:
            string  summary: text summary

    """
    sentence = sent_tokenize(article)
    corpus = []

    for i in range(len(sentence)):
        sen = re.sub('[^а-яА-Я]', " ", sentence[i])  
        sen = sen.lower()                            
        sen=sen.split()                         
        sen = ' '.join([i for i in sen if i not in stopwords.words('russian')])   
        corpus.append(sen)
        
    n=300
    all_words = [i.split() for i in corpus]
    model = Word2Vec(all_words, min_count=1,size=n)

    sen_vector=[]
    for i in corpus:
        plus=0
        for j in i.split():
            plus+=model.wv[j]
        plus = plus/len(plus)
        sen_vector.append(plus)
        
    n_clusters = n_sentences
    kmeans = KMeans(n_clusters, init = 'k-means++', random_state = 42)
    y_kmeans = kmeans.fit_predict(sen_vector)

    my_list=[]
    for i in range(n_clusters):
        my_dict={}
        for j in range(len(y_kmeans)):
            if y_kmeans[j]==i:
                my_dict[j] =  distance.euclidean(kmeans.cluster_centers_[i],sen_vector[j])
        min_distance = min(my_dict.values())
        my_list.append(min(my_dict, key=my_dict.get))
                                
    summary = []
    for i in sorted(my_list):
        summary.append(sentence[i])
    
    summary = ' '.join(summary)
    return summary


def kmeans_ranging(X_pred):
    
    model_filename = "kmeans.pkl"
    with open(model_filename,'rb') as file:
        f_kmeans = pickle.load(file)
        
    n_clusters = 400
    y_kmeans = f_kmeans.fit_predict(X_pred)

    lbl_df = pd.DataFrame(f_kmeans.labels_).value_counts()

    my_list=[]
    for i in [i[0] for i in lbl_df[lbl_df >= 35].index]:
        my_dict={}

        for j in range(len(y_kmeans)):

            if y_kmeans[j]==i:
                my_dict[j] =  distance.euclidean(f_kmeans.cluster_centers_[i],X_pred[j])
        min_distance = min(my_dict.values())
        my_list.append(min(my_dict, key=my_dict.get))
        
    with open(model_filename,'wb') as file:
        pickle.dump(f_kmeans,file)
        
    return my_list

# category, timestampStart, timestampEnd
@app.route('/get_digest', methods = ['GET'])
def get_digest():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        category = json['category']
        timestampStart = json['timestampStart']
        timestampEnd = json['timestampEnd']

        conn = psycopg2.connect(dbname='db', user='postgres', 
                        password='postgres', host='localhost')
        cur = conn.cursor()

        k = 3
        decoded_rows = []
        cur.execute("""SELECT TIMESTAMP,ID,ML FROM newsdata WHERE TIMESTAMP > %s AND TIMESTAMP < %s """, (timestampStart, timestampEnd))
        obj = cur.fetchall()
        for row in obj:
            ml = ModelServiceAnswer()
            ml.ParseFromString(row[2])

            for item in ml.Categories:
                if item.Category == category:
                    decoded_rows.append((item.Probability, row[1]))
        
        decoded_rows.sort()
        size = len(decoded_rows)
        real_size = min(size, k)

        best_rows = decoded_rows[:real_size]

        best_ids = ''
        for item in best_rows:
            best_ids+="\'"
            best_ids+=str(item[1])
            best_ids+="\'"
            best_ids+=', '

        best_ids = best_ids[:-2]

        answer = []
        cur.execute("""SELECT TITLE,BODY,ID FROM newsdata WHERE ID IN (""" + best_ids + """)""")
        obj = cur.fetchall()
        for row in obj:
            news = {
                'Title': row[0],
                'Body': row[1]
            }
            answer.append(news)
        
        return jsonify({'data': answer})
        
    return jsonify({'data': 'not ok'})

@app.route('/get_trend', methods = ['GET'])
def get_trend():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        timestampStart = json['timestampStart']
        timestampEnd = json['timestampEnd']

        conn = psycopg2.connect(dbname='db', user='postgres', 
                        password='postgres', host='localhost')
        cur = conn.cursor()

        all_embeds = []
        ids = []
        cur.execute("""SELECT ID,ML FROM newsdata WHERE TIMESTAMP > %s AND TIMESTAMP < %s """, (timestampStart, timestampEnd))
        obj = cur.fetchall()
        for row in obj:
            ids.append(row[0])
            ml = ModelServiceAnswer()
            ml.ParseFromString(row[1])

            local_embed = []
            for item in ml.Embeddings:
                local_embed.append(item)
            all_embeds.append(local_embed)

        best_rows = []
        my_list = kmeans_ranging(all_embeds)

        # logging.warning(my_list)
        # logging.warning(ids)

        for item in my_list:
            best_rows.append(ids[item])

        best_ids = ''
        for item in best_rows:
            best_ids+="\'"
            best_ids+=str(item)
            best_ids+="\'"
            best_ids+=', '

        best_ids = best_ids[:-2]

        answer = []

        cur.execute("""SELECT TITLE,BODY,ID FROM newsdata WHERE ID IN (""" + best_ids + """)""")
        obj = cur.fetchall()
        for row in obj:
            body = summarize(row[1])
            news = {
                'Title': row[0],
                'Body': body
            }
            answer.append(news)
        
        return jsonify({'data': answer})

    return jsonify({'data': 'not ok'})


if __name__ == '__main__':
  
    app.run(debug = True, host='0.0.0.0', port=8002)
