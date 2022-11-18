import spacy
from spacy import displacy
# Move Firestore db connection to another file
from google_reddit_scrape import *

nlp = spacy.load("en_core_web_sm")

# Testing with a specific post_id
TEST_POST_ID = "be5rj"

# Create a reference to the comments collection
comments_ref = db.collection(REDDIT_POSTS_COLLECTION).document(TEST_POST_ID).collection(COMMENTS_COLLECTION)

# Create a query against the collection for the top comment
query_ref = comments_ref.where("comment_rank", "==", 0).get()

text = ""

for comment in query_ref:
    text += comment.to_dict()["top_level_comment"]

doc = nlp(text)
displacy.serve(doc, style="ent")