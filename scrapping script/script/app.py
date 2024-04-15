from scrapping import run
from flask import Flask, request
app = Flask(__name__)
# Add Flask api endpoint for running the scrapping
@app.route('/scrap', methods=["POST"])
def add_guide():
    response = run(
        username = request.json['username'],
        password = request.json['password'],
        posts_size = request.json['posts_size'],
        search = request.json['search'],
        label = request.json['label']
    )
    return response

@app.route('/database', methods=["GET"])
def add_guide():
    return 

if __name__ == "__main__":
    app.run()