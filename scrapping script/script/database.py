from mysql.connector import connect
import os

"""
CREATE TABLE UserPosts (
    usertag VARCHAR(255),
    date_time DATETIME,
    post TEXT,
    label VARCHAR(50),
    PRIMARY KEY (usertag,date_time)
);
"""

class POST_ORM:
    def __init__(self):
        self.connection = connect(
            user=os.environ.get("MYSQL_USER"), 
            password=os.environ.get("MYSQL_PASSWORD"),
            host=os.environ.get("MYSQL_HOST"),
            port=os.environ.get("MYSQL_PORT"),
            database=os.environ.get("MYSQL_DATABASE"))
    """
    INSERT IGNORE INTO UserPosts (usertag, date_time, post, label)
    VALUES ('usertag_value', '2024-04-11 12:00:00', 'This is a post.', 'label_value');
    """
    def save(self,post):
        sql = f"INSERT INTO UserPosts (usertag, date_time, post, label) VALUES (%s, %s, %s, %s);"
        values = (post.usertag, post.time_date, post.text, post.label)
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        cursor.close()