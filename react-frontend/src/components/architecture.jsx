import React, { Component } from "react";

class Architecture extends Component {
  render() {
    return (
      <div className="jumbotron jumbotron-fluid">
        <div className="container">
          <h1 className="display-4">Architecture</h1>
          <p className="lead">
            I'm going to be using{" "}
            <a href="https://cloud.google.com/gcp/" target="_blank">
              Google Cloud Services
            </a>{" "}
            for developing this solution. The priority is to use serverless
            technology, but when not available or if it does not fit, a no-ops
            solution will be adopted.
          </p>
          <img src="/no-name-yet.png" />
        </div>
      </div>
    );
  }
}

export default Architecture;
