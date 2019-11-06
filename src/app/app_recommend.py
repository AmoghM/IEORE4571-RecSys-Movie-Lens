from flask import Flask, request, render_template, send_file
from tmdbv3api import TMDb, Movie
from PIL import Image
import requests, os
from io import BytesIO
from io import StringIO

tmdb = TMDb()
tmdb.api_key = '8b7c66ca53f19e908507247a0b0d1b00'
tmdb.language = 'en'

app = Flask(__name__,template_folder='./template')

@app.route('/fetch', methods=['POST'])
def fetch():
    projectpath = request.form['projectFilepath']
    id = request.args.get(projectpath)
    print(id)
    movie = Movie()
    m = movie.details(343611)
    url = "http://image.tmdb.org/t/p/w500/"+m.poster_path
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save('static/movie.jpg')
    return render_template("image.html")

@app.route('/')
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run()