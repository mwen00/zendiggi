from sqlalchemy.orm import Session

from db.base_class import Base
from db.session import engine


# FIRST_SUPERUSER = "admin@zendiggi.com"

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    ...
    # TODO: The above doesn't work! I have to run a migration to create initial tables. 
    # TODO: Define any initial seed logic
    