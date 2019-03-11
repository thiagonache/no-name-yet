import React, { Component } from "react";

class About extends Component {
  render() {
    return (
      <div className="jumbotron jumbotron-fluid">
        <div className="container">
          <h1 className="display-4">How am I?</h1>
          <p className="lead">
            I'm system administrator and will write more about me when inspired
            :P
          </p>
          <h1 className="display-4">Source code</h1>
          <p>
            You can found it{" "}
            <a href="https://github.com/thiagonache/no-name-yet">here</a>.
          </p>
        </div>
      </div>
    );
  }
}

export default About;
