from insert import insert_data_to_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from type import God, ChatRequest, GetEmbeddingsRequest
from db import Neo4jDB
from dotenv import load_dotenv
from helpers import get_embedding
from search import SearchAgent
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is running"}

driver = Neo4jDB().get_db()

@app.get("/health")
async def health():
    
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 1")
        return {"message": "DB is running"}

import csv
from type import God

def load_gods_from_csv(csv_path="gods.csv"):
    gods = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            god = God(**row)
            gods.append(god)
    return gods


@app.post("/chat")
async def chat(request: ChatRequest):
    search_agent = SearchAgent()
    response = search_agent.search(request.text)
    print(response)
    return {"message": response}
    

@app.post("/insert_csv")
async def insert_csv():
    gods = load_gods_from_csv("gods.csv")
    insert_data_to_db(gods)
    return {"message": f"{len(gods)} gods inserted successfully"}


@app.post("/get-embeddings")
async def get_embeddings(request: GetEmbeddingsRequest):
    return get_embedding(request.name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
