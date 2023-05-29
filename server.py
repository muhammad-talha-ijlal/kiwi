import csv
from datetime import datetime
from flask import Flask, request, render_template, abort, Response
from scrapper import scrap
from mat import plot
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

id = 0

CSV_FILE = 'client_quality.csv'
CSV_HEADERS = ['Timestamp', 'IP Address', 'User Agent', 'URL']

def save_quality_info(data):
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writerow(data)

@app.route('/', methods=['GET'])
def main_page():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    url = request.url
    quality_data = {
        'Timestamp': timestamp,
        'IP Address': ip_address,
        'User Agent': user_agent,
        'URL': url,
    }
    save_quality_info(quality_data)

    return render_template('index.html')
    
@app.route('/search', methods=['POST'])
def search_fiverr():
    global id

    keywords = request.json['keywords']
    data = scrap(keywords)
    id += 1
    plot(data, id)
    file = f'visualization{id}.pdf'
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            response = Response(f.read(), content_type='application/pdf')
            response.headers['Content-Disposition'] = f'attachment; filename={file}'
            return response
    abort(404)

if __name__ == '__main__':
    app.run()
