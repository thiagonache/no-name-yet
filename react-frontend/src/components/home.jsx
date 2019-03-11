import React, { Component } from "react";

class Home extends Component {
  render() {
    return (
      <div className="jumbotron jumbotron-fluid">
        <div className="container">
          <h1 className="display-4">Full-stack project</h1>
          <p className="lead">
            The main idea is to start a project that the community thinks would
            be useful. I want to spend my personal time developing an open
            source full-stack solution, so I've started by creating a simple
            website and poll module to collect info.
          </p>
          <h2 className="display-6">How you can contribute</h2>
          <p>
            The first step is to define what this tool is going to be. I want to
            create something that myself and other people can use on a daily
            basis, not just something that won't be used.
          </p>
          <ul>
            <li>
              What have you been missing from the tools provided by the cloud
              providers?
            </li>
            <li>
              Where have you been spending your time doing tasks that could be
              automated?
            </li>
            <li>
              What have you implemented by yourself but don't want to spend time
              managing it?
            </li>
            <li>What idea do you have?</li>
          </ul>
        </div>
      </div>
    );
  }
}

export default Home;
