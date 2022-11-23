import spacy
from spacy import displacy
# Move Firestore db connection to another file
from google_reddit_scrape import *

nlp = spacy.load("en_core_web_sm")

# Testing with a specific post_id
# TEST_POST_ID = "be5rj"

# Create a reference to collections
posts_ref = db.collection(REDDIT_POSTS_COLLECTION)
# comments_ref = db.collection(REDDIT_POSTS_COLLECTION).document(TEST_POST_ID).collection(COMMENTS_COLLECTION)

# Create a query against the desired collection
posts_query_ref = posts_ref.where("google_search_rank", "==", 0).get()
# comments_query_ref = comments_ref.where("comment_rank", "==", 0).get()

text = ""

for post in posts_query_ref:
    text += f"\n----------- NEW POST {post.id} -----------\n"
    comments_ref = db.collection(REDDIT_POSTS_COLLECTION).document(post.id).collection(COMMENTS_COLLECTION)
    comments_query_ref = comments_ref.get()

    for comment in comments_query_ref:
        data = comment.to_dict()
        text += f"\n----------- TOP LEVEL COMMENT for POST {post.id} -----------\n"
        text += data["top_level_comment"] + "\n----------- REPLIES -----------\n" + data["replies"]


doc = nlp(text)
displacy.serve(doc, style="ent")