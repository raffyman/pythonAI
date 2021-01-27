import React from "react";
import MessageGallery from "./MessageGallery";

export default class Message extends React.Component {
  render() {
    const { message } = this.props;
    let username = message.from;

    let pull = "pull-left";
    let src = "./assets/robot.png";

    if (message.from == "botsApiChannel:") {
      username = "Bot";
    }

    if (message.me) {
      pull = "pull-right";
      src = "./assets/me.png";
    }

    return (
      <div>
        <div className={pull} style={{padding: "10px" }}>
          <img src={src} width="30" />
        </div>
          <div
            className={pull + " d-flex align-self-center"}
            style={{
              maxWidth:"50%",
              backgroundColor: "#064740",
              padding: "5px",
              marginTop: "10px",
              borderRadius: "10px",
            }}
          >
            {/* <b style={{ color: "white" }}>{username}</b> */}
            <p style={{ margin: 0, color: "white" }}>{message.message}</p>
          </div>
        <div className="clearfix"></div>
      </div>
    );
  }
}
