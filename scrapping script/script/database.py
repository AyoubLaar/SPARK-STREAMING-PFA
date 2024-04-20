from google.cloud import firestore

class POST_ORM:

    counter = 0

    def __init__(self):
        self.connection = firestore.Client()
  
    def save(self,post):
        data = { "post":post.text, "label":post.label}
        self.connection.collection("posts").document(post.usertag+" "+post.time_date).create(data)
        POST_ORM.counter = POST_ORM.counter + 1
        
    def close(self):
        self.connection.close()


if __name__ == "__main__":
    from dotenv import load_dotenv,find_dotenv
    load_dotenv(find_dotenv())
    class test_class:
        def __init__(self) -> None:
            self.text = "testing"
            self.label = "l"
            self.usertag = "ayoub"
            self.time_date = "time_test"
    post_orm = POST_ORM()
    post_orm.save(test_class())
    pass