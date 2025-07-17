from pydantic_ai import Agent
from dotenv import load_dotenv
from base import get_openai_client
from helpers import get_embedding
from db import Neo4jDB
import json

load_dotenv()

class SearchAgent(Agent):
    def __init__(self): 
        self.name = "Search Agent"
        self.description = "A search agent that uses a vector index to search Sanatan Dharma knowledge graph"
        self.model = get_openai_client()
        self.driver = Neo4jDB().get_db()

    def search(self, query: str):
        agent_prompt = """
        You are a wise and knowledgeable agent with access to a rich knowledge graph of Sanatan Dharma deities.  
This graph contains nodes representing various divine names, each with the following properties:

- `belongs_to`: The primary deity or tradition the name is associated with (e.g., Shiva, Devi, Narayan)
- `name`: The specific name or epithet of the deity
- `meaning`: The meaning or spiritual significance of the name
- `mantra`: The mantra associated with this name
- `sanskrit`: The mantra written in Sanskrit script

NOTE: This should have only one data, dont create multple json.

When a user makes a query, you will use the relevant data retrieved from the graph to construct a short, meaningful story about the deity or deities.  
Your response must always follow this format:
{
  "story": "Your generated story here"
}
        """

        # 1. Embed the query
        query_embedding = get_embedding(query)

        # 2. Query Neo4j vector index
        with self.driver.session() as session:
            result = session.run(
                """
                CALL db.index.vector.queryNodes('devine_index', $topK, $embedding)
                YIELD node, score
                RETURN node.belongs_to AS belongs_to, node.name AS name, node.meaning AS meaning,
                       node.mantra AS mantra, node.sanskrit AS sanskrit
                """,
                embedding=query_embedding,
                topK=5
            )

            nodes = [record.data() for record in result]

        if not nodes:
            return {"result": []}

        # 3. Prepare context for the LLM
        context = f"Here is the information retrieved from the graph:\n{json.dumps(nodes, indent=2)}"

        # 4. Run completion with context + user query
        response = self.model.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": agent_prompt},
                {"role": "user", "content": f"{context}\n\nUser Query: {query}"}
            ],
            temperature=0.3,
        )
        
        print(f"Response: {response.choices[0].message.content}")

        return response.choices[0].message.content
