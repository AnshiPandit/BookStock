from fastapi import FastAPI
from src.books.routes import book_router
# for lifespan even
from contextlib import asynccontextmanager
from src.db.main import init_db

from fastapi.middleware.cors import CORSMiddleware

# creating LIFESPAN EVENT
# lifespan even is an event that runs for the enitrty of our app
# we want the db connection to be started from the launch of our app
@asynccontextmanager
# it has to be a async func with async keyword
async def life_span(app:FastAPI):# this func takes an app instance as parameter
    print(f"server is starting...")
    # The await keyword in Python is used to pause execution of a coroutine until the awaited asynchronous operation is complete. It allows non-blocking execution in an async function.
    # wheneven you call an async func you need to call it with await
    await init_db()
    # yield keyword is going to determine which code is going to run first and which will run later or at the end of server
    # using the asynccontextmanager decorator means the code above yield keyword runs at the start of server and below it at the stop
    yield 
    print(f"server has been stopped")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version= version,
    # the life_span event has to be resgistered to the fastapi instance
    lifespan=life_span
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])