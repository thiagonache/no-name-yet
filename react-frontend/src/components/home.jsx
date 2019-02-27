import React, { Component } from "react";
import { NavLink } from "react-router-dom";

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
            website and poll application.
          </p>
          <h2 className="display-6">How you can contribute</h2>
          <p>
            The first step is to define what this tool is going to be. I want to
            create something that myself and other people can use on a daily
            basis, not just something that won't be used. So, first of all, the
            main question is if you are interested. Please, visit{" "}
            <NavLink to="/poll">pool.</NavLink>
          </p>
          <p>
            Currently, there's no authentication and the vote API is public to
            the world since it is just to see if I will go further with this
            project. If we have any issue regarding attackers (people that
            really does not have anything to do), I will reset the counters and
            require authentication. Maybe more restrictions.
          </p>
          <p>
            If we decide to go ahead with this project, I'll create a new poll
            with items/ideas for what this solution should be. Then, to add a
            new item you need to login with your Google or Facebook account. To
            vote the person still be able to keep anonymous.
          </p>
          <p>
            <ul>
              <li>
                What have you been missing in the tools provided by the cloud
                providers?
              </li>
              <li>
                Where have you been spending your time doing tasks that could be
                automated?
              </li>
              <li>
                What have you implemented by yourself but don't want to spend
                time managing it?
              </li>
              <li>What idea do you have?</li>
            </ul>
          </p>
        </div>
      </div>
    );
  }
}

export default Home;
