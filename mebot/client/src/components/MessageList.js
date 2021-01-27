import React from "react";

import Message from "./Message";

export default class MessageList extends React.Component {
  render() {
    const { messages } = this.props;
    return (
      <div className="panel panel-default" style={{ marginBottom: "0px" }}>
        <div className="panel-heading" style={{ backgroundColor: "#232D36" }}>
          <h3 className="panel-title" style={{ color: "white" }}>
            MeBot
          </h3>
        </div>
        <div
          id="area-message"
          className="panel-body"
          style={{
            height: "450px",
            overflowY: "scroll",
            backgroundColor: "#05181F",
          }}
        >
          {messages.map((message, index) => (
            <Message key={index} message={message} />
          ))}
        </div>
      </div>
    );
  }
}
