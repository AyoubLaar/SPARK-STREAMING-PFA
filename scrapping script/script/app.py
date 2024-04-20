import scrapping
from database import POST_ORM
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

# Add Flask api endpoint for running the scrapping
@app.route('/scrap', methods=["POST"])
def scrap():
    try:
        scrapping.run(
        username = request.json['username'],
        password = request.json['password'],
        posts_size = int(request.json['posts_size']),
        search = request.json['search'],
        label = request.json['label']
        )
        return jsonify(success=True)
    except:
        return jsonify(success=False,message="check log file")
    
@app.route('/test_database', methods=["GET"])
def test_database():
    try: 
        post_orm = POST_ORM()
        post_orm.close()
        return jsonify(success=True)
    except:
        return jsonify(success=False,message=traceback.format_exc())
        
@app.route('/test_all', methods=["POST"])
def test_all():
    username = request.json['username']
    password = request.json['password']
    search = request.json['search']
    message = ' '.join(scrapping.test_all(username,password,search))
    return jsonify(message=message)

if __name__ == "__main__":
    app.run()