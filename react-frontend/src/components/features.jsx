import React, { Component } from "react";

class Features extends Component {
  render() {
    return (
      <div className="jumbotron jumbotron-fluid">
        <div className="container">
          <h1 className="display-4">Features</h1>
          <p className="lead">
            The main principle for this application is security.
          </p>
          <p>
            <ul>
              <li>Encrypt data in transit.</li>
              <li>Encrypt data at rest.</li>
              <li>
                Each user has it own data encrypted with dedicated KMS key.
              </li>
              <li>Under construction</li>
            </ul>
          </p>
        </div>
      </div>
    );
  }
}

export default Features;
