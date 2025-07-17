from db import Neo4jDB
from type import God
from db import Neo4jDB
from helpers import get_embedding



def create_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:DivineName) REQUIRE n.name IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Deity) REQUIRE n.name IS UNIQUE")
    
def insert_data(tx,data):
    # create node for name with the property meaning, mantra, sanskrit
    print(f"Inserting data for {data.name}")
    tx.run(
        """
        MERGE (n:DivineName {name: $name})
        SET n.meaning = $meaning,
            n.mantra = $mantra,
            n.sanskrit = $sanskrit
        """,
        name=data.name,
        meaning=data.meaning,
        mantra=data.mantra,
        sanskrit=data.sanskrit,
    )
    
def insert_deity_node(tx, deity_name):
    tx.run(
        """
        MERGE (:Deity {name: $name})
        """,
        name=deity_name
    )
    

def add_searchable_property(tx):
    print("Adding searchable property to the nodes")
    tx.run(
        """
        MATCH (n)
        WHERE n.embedding IS NOT NULL
        SET n.searchable = true
        """,
    )
    
def insert_relationship(tx, data):
    print(f"Inserting relationship for {data.name} and {data.belongs_to}")
    tx.run(
        """
        MATCH (a:DivineName {name: $name})
        MATCH (b:Deity {name: $belongs_to})
        MERGE (a)-[:BELONGS_TO]->(b)
        """,
        name=data.name,
        belongs_to=data.belongs_to
    )



def add_embedding_to_data(tx, name: str, embedding: list[float]):
    print(f"Adding embedding to {name}")
    tx.run(
        """
        MATCH (n:DivineName {name: $name})
        SET n.embedding = $embedding
        """,
        name=name,
        embedding=embedding
    )   
    
def add_embedding_to_deity(tx, name: str, embedding: list[float]):
    print(f"Adding embedding to {name}")
    tx.run(
        """
        MATCH (n:Deity {name: $name})
        SET n.embedding = $embedding
        """,
        name=name,
        embedding=embedding
    )
    
def insert_data_to_db(data):
    db = Neo4jDB()
    # 1. Create constraints in a separate transaction
    with db.get_session() as session:
        with session.begin_transaction() as tx:
            create_constraints(tx)
            tx.commit()

    # 2. Insert nodes in a new transaction
    with db.get_session() as session:
        with session.begin_transaction() as tx:
            for god in data:
                insert_data(tx, god)
                insert_deity_node(tx, god.belongs_to)
                insert_relationship(tx, god)
                text_for_embedding = f"{god.name} {god.meaning} {god.mantra}"
                embedding = get_embedding(text_for_embedding)
                add_embedding_to_data(tx, god.name, embedding)  
                add_embedding_to_deity(tx, god.belongs_to, embedding)
                
            # Add searchable property to the nodes
            add_searchable_property(tx)
            tx.commit()

    print("Data and relationships inserted successfully")
    db.close()
    
    