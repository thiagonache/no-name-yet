import React, { Component } from "react";
import { Route, Redirect, Switch } from "react-router-dom";
import "./App.css";
import NavBar from "./components/navBar";
import Home from "./components/home";
import Features from "./components/features";
import Architecture from "./components/architecture";
import MainPoll from "./components/mainPoll";
import About from "./components/about";
import NotFound from "./components/notFound";

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <NavBar />
        <main className="container">
          <Switch>
            <Route path="/home" component={Home} />
            <Route path="/features" component={Features} />
            <Route path="/architecture" component={Architecture} />
            <Route path="/poll" component={MainPoll} />
            <Route path="/about" component={About} />
            <Route path="/not-found" component={NotFound} />
            <Redirect from="/" exact to="/home" />
            <Redirect to="/not-found" />
            <Redirect to="/home" />
          </Switch>
        </main>
      </React.Fragment>
    );
  }
}

export default App;
