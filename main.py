from flask import Flask, render_template, request
import requests

app = Flask(__name__)



def get_book_cover(cover_i):
    if cover_i:
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
        return cover_url
    return None



@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/search')
def search_by_name():
    return render_template('search.html', get_book_cover=get_book_cover)



@app.route('/', methods=['GET', 'POST'])
def index():
    books = []
    if request.method == 'POST':
        search_query = request.form['search']
        books = search_books(search_query)
    return render_template('search.html', books=books, get_book_cover=get_book_cover)


def search_books(query):
    base_url = 'http://openlibrary.org/search.json'
    params = {'q': query}
    response = requests.get(base_url, params=params)
    data = response.json()

    return data.get('docs', [])

if __name__ == '__main__':
    app.run(debug=True)
