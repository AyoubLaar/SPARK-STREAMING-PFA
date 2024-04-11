import mysql.connector
import os

"""
CREATE TABLE UserPosts (
    user_id INT NOT NULL AUTO_INCREMENT,
    usertag VARCHAR(255),
    date_time DATETIME,
    post TEXT,
    label VARCHAR(50),
    PRIMARY KEY (user_id)
);
"""


class POST_ORM:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                user=os.environ.get("MYSQL_USER"), 
                password=os.environ.get("MYSQL_PASSWORD"),
                host=os.environ.get("MYSQL_HOST"),
                database=os.environ.get("MYSQL_DATABASE"))
        except:
            print("Connection Error")
            exit()
    """
    INSERT IGNORE INTO UserPosts (usertag, date_time, post, label)
    VALUES ('usertag_value', '2024-04-11 12:00:00', 'This is a post.', 'label_value');
    """
    def save(self,usertag,datetime,text,label):
        sql = f"INSERT INTO UserPosts (usertag, date_time, post, label) VALUES ('{usertag}', '{datetime}', '{text}.', '{label}');"
        self.connection.quer

def post_to_values(post):
    pass