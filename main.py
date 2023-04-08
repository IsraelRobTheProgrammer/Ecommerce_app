from fastapi import FastAPI
from models import item, user, review
from sql_database import engine

from routes import items, users, reviews

app = FastAPI()  # initializing the app

# create the tables
item.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
review.Base.metadata.create_all(bind=engine)

# adding external routes
app.include_router(items.router)
app.include_router(users.router)
app.include_router(reviews.router)
