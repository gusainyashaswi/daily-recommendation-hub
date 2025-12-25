from flask import Flask, render_template, request
import csv
from flask import redirect

app = Flask(__name__)

def score_item(item, liked_titles):
    score = popularity_score(item['popularity'])
    if item['title'] in liked_titles:
        score += 2
    return score


def load_preferences():
    preferences = []
    try:
        with open('data/user_preferences.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                preferences.append(row)
    except FileNotFoundError:
        pass
    return preferences


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

    recommendations = [item for item in data if item['mood'] == mood]

    # take top 5
    recommendations = recommendations[:5]

    return render_template(
        'results.html',
        recommendations=recommendations,
        content_type=content_type
    )


@app.route('/feedback', methods=['POST'])
def feedback():
    title = request.form['title']
    content_type = request.form['content_type']
    action = request.form['action']

    with open('data/user_preferences.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([title, content_type, action])

    return redirect('/')


    recommendations = recommendations[:5]
    return render_template(
    'results.html',
    recommendations=recommendations,
    content_type=content_type
)



if __name__ == '__main__':
    app.run(debug=True)
