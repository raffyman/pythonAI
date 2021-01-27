import React from "react";
import axios from "axios";

import MessageList from "./components/MessageList";
import MessageInput from "./components/MessageInput";

import "./App.css";
import { Neo4jGraphRenderer } from "neo4j-graph-renderer";
import Graph from "./components/Graph";
class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      messages: [],
      increment: 0,
    };

    this.newMessage = this.newMessage.bind(this);
  }

  componentDidUpdate() {
      var areaMessage = document.getElementById("area-message");
      areaMessage.scrollTop = areaMessage.scrollHeight
      // areaMessage.scrollIntoView({ behavior: "smooth" });
  }

  // componentWillMount() {
  //   axios({
  //     method: "get",
  //     url:
  //       "https://snatchbot.me/channel/api/id19475/appdino20180603/apsdino03062018?user_id=12345",
  //     responseType: "json",
  //   }).then((response) => {
  //     const messages = response.data.messages;
  //     const data = [];

  //     messages.map((message, index) => {
  //       if (message.message !== "") {
  //         data.push(message);
  //       }
  //     });
  //     this.setState({
  //       messages: data,
  //     });

  //     console.log(data);
  //   });
  // }

  newMessage(message) {
    const { increment, messages } = this.state;

    this.setState({
      messages: [...messages, message],
      increment: increment + 1,
    });

    // areaMessage.scrollTop = areaMessage.scrollHeight;
    this.sendMessage(message.message);
    // const toBottom = areaMessage.scrollHeight * increment;
    // alert("called")
    // area-message
    // areaMessage.scrollTo(0, toBottom);
  }

  sendMessage(message) {
    axios.post("http://127.0.0.1:5000/",{
        usr_msg: message,
    }
    ).then((response) => {
      console.log(response)
      var results = this.state.messages.concat({from: "mebot", message: response.data });
      this.setState({
        messages: results,
      });
    });
  }

  render() {
    const { messages } = this.state;
    return (
       <div
        className="container"
        style={{
          marginTop: "50px",
          marginBottom: "50px",
          backgroundColor: "#1f2933",
        }}
      >
        <div className="row">
          <div className="col-xs-6 col-sm-6 col-md-6 col-lg-6">
            <Graph />
          </div>
          <div className="col-xs-6 col-sm-6 col-md-push-1 col-md-5 col-lg-5">
            <MessageList messages={messages} />
            <MessageInput newMessage={this.newMessage} />
          </div>
        </div>

        <div className="row">
          <h3 className="text-primary">mebot</h3>
          <h4 className="text-muted">
            Haider Ali Khichi - SP17-BCS-038
          </h4>
          <h4 className="text-muted">
            Muhammad Hassan Mustafa - SP17-BCS-065
          </h4>
          <h4 className="text-muted">
            Muhammad Rafay Khalid - SP17-BCS-044
          </h4>
        </div>
      </div>
    );
  }
}

export default App;
