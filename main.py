from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Sample user data (for demonstration purposes)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# Open Library API base URL
OPEN_LIBRARY_API_BASE = 'http://openlibrary.org/search.json'

def get_book_cover(cover_i):
    if cover_i:
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
        return cover_url
    return None

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            # In a real application, you would use a session to keep the user logged in.
            return redirect(url_for('search_by_name'))
        
        return "Invalid login credentials"
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # In a real application, you would add the new user to the database with hashed password.
        users[username] = password
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')


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
    params = {'q': query}
    response = requests.get(OPEN_LIBRARY_API_BASE, params=params)
    data = response.json()
    return data.get('docs', [])

if __name__ == '__main__':
    app.run(debug=True)
