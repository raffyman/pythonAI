from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123456"))


def create_friend_of(tx, name, friend):
    query = 'CREATE (a:Person)-[:KNOWS]->(f:Person {name:"%s"}) return a,f' % friend
    print(query)
    tx.run(query)


with driver.session() as session:
    session.write_transaction(create_friend_of, "Alice", "Bob")

with driver.session() as session:
    session.write_transaction(create_friend_of, "Alice", "Carl")

driver.close()
