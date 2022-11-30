# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  
from app.models.location import Location
from app.models.reddit_post import RedditPost
from app.models.reddit_comment import RedditComment
