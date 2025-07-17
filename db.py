from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jDB:
    
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def close(self):
        self.driver.close()

    def get_db(self):
        return self.driver

    def get_session(self):
        return self.driver.session()
    
    async def test_connection(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 1")
            return result
    