import scrapping
from database import POST_ORM
from flask import Flask, request, jsonify
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)

# Add Flask api endpoint for running the scrapping
@app.route('/scrap', methods=["POST"])
def scrap():
    try:
        scrapping.run(
        username = request.json['username'],
        password = request.json['password'],
        posts_size = request.json['posts_size'],
        search = request.json['search'],
        label = request.json['label']
        )
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/test_database', methods=["GET"])
def test_database():
    try:
        POST_ORM()
        return jsonify(success=True)
    except:
        return jsonify(success=False)
        
@app.route('/test_search', methods=["POST"])
def test_search():
    username = request.json['username']
    password = request.json['password']
    search = request.json['search']
    message = ' '.join(scrapping.test_search(username,password,search))
    return jsonify(message=message)

if __name__ == "__main__":
    app.run()