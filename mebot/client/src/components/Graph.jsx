import { Neo4jGraphRenderer } from "neo4j-graph-renderer";
import React from "react";

export default class Graph extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    // return null
    return (
      <Neo4jGraphRenderer
        url="http://3.90.84.205:34733"
        user="neo4j"
        password="swaps-alloy-classrooms"
        query="MATCH (n)-[r]->(m) RETURN n,r,m"
      />
    );
  }
}
