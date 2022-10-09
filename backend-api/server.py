from flask import Flask, jsonify, request

from contracts_pb2 import ModelServiceAnswer

import psycopg2
import logging
  
app = Flask(__name__)

# category, timestampStart, timestampEnd
@app.route('/get_digest', methods = ['GET'])
def get_users():
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
        logging.warning(type(best_ids))
        logging.warning(best_ids)

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

if __name__ == '__main__':
  
    app.run(debug = True, host='0.0.0.0', port=8002)
