from flask import Flask, jsonify, request

from contracts_pb2 import ModelServiceAnswer
  
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
        for row in cur.execute("""SELECT TIMESTAMP,ID,ML FROM newsdata WHERE TIMESTAMP > %s AND TIMESTAMP < %s """, (timestampStart, timestampEnd)):
            ml = ModelServiceAnswer()
            ml.ParseFromString(row[2])

            for item in ml.Categories:
                if item.Category == category:
                    decoded_rows.append((item.Probability, row[1]))
        
        sort(decoded_rows)

        size = len(decoded_rows)
        real_size = max(size, k)

        best_rows = decoded_rows[:real_size]
        best_ids = ''
        for item in best_ids:
            best_ids+=str(item[1])
            best_ids+=', '
        best_ids = best_ids[:-2]

        answer = {}
        for row in cur.execute(""" SELECT TITLE,BODY,ID FROM newsdata WHERE ID IN (%s))""", best_ids):
            news = {
                'Title': row[0],
                'Body': row[1]
            }
            answer.add(news)
        
        return jsonify({'data': answer})
        
    return jsonify({'data': 'not ok'})

if __name__ == '__main__':
  
    app.run(debug = True, host='0.0.0.0', port=8002)
