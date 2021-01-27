import React from "react";

export default class MessageInput extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      from: "hassan",
      message: "",
      me: true,
    };

    this.handleOnChange = this.handleOnChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault()

    if (this.state.message) { 
      this.props.newMessage(this.state);

      this.setState({
        message: "",
      });
    }
  }

  handleOnChange(e) {
    const target = e.target;

    this.setState({
      [target.name]: target.value,
    });
  }

  render() {
    const { from, message } = this.state;
    return (
      <form
        method="POST"
        style={{ backgroundColor: "#1f2933", marginTop: "10px" }}
        onSubmit={this.handleSubmit}
      >
        <div className="input-group">
          <input
            type="text"
            name="message"
            className="form-control"
            placeholder="Message..."
            style={{
              backgroundColor: "#2C373D",
              color: "white",
            }}
            value={message}
            onChange={this.handleOnChange}
            autoFocus="true"
          />

          <span className="input-group-btn">
            {/* <button
              type="btn btn-primary submit"
              style={{ backgroundColor: "#25D366", padding:'10' }}
            >
              sdfsdf
            </button>  */}
            <button type="button" style={{backgroundColor: "#25D366", color:'white'}} class="btn btn-default">
  <span class="glyphicon glyphicon-send" aria-hidden="true"></span>
</button>
           </span>
        </div>
      </form>
    );
  }
}
