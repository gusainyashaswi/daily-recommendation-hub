from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_data(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    content_type = request.form['content_type']
    mood = request.form['mood']

    file_map = {
        'movies': 'data/movies.csv',
        'songs': 'data/songs.csv',
        'books': 'data/books.csv'
    }

    data = load_data(file_map[content_type])

    recommendations = [
        item for item in data if item['mood'] == mood
    ]

    recommendations = recommendations[:5]

    return render_template(
        'results.html',
        recommendations=recommendations
    )

if __name__ == '__main__':
    app.run(debug=True)
