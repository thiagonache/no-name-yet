// community modules
import React, { Component } from "react";
import { Route, Redirect, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";

// local modules
import NavBar from "./components/navBar";
import Home from "./components/home";
import Features from "./components/features";
import Architecture from "./components/architecture";
import MainPoll from "./components/mainPoll";
import About from "./components/about";
import NotFound from "./components/notFound";
import RegisterForm from "./components/registerForm";
import LoginForm from "./components/loginForm";
import Logout from "./components/logout";
import auth from "./services/authService";
//import ProtectedRoute from "./components/common/protectedRoute";

// CSS
import "./App.css";
import "react-toastify/dist/ReactToastify.css";

class App extends Component {
  state = {};

  componentDidMount() {
    const user = auth.getCurrentUser();
    this.setState({ user });
  }

  render() {
    const { user } = this.state;
    return (
      <React.Fragment>
        <ToastContainer />
        <NavBar user={user} />
        <main className="container">
          <Switch>
            <Route path="/home" component={Home} />
            <Route path="/features" component={Features} />
            <Route path="/architecture" component={Architecture} />
            <Route path="/poll" render={() => <MainPoll user={user} />} />
            <Route path="/register" component={RegisterForm} />
            <Route path="/login" component={LoginForm} />
            <Route path="/logout" component={Logout} />
            <Route path="/about" component={About} />
            <Route path="/not-found" component={NotFound} />
            <Redirect from="/" exact to="/home" />
            <Redirect to="/not-found" />
          </Switch>
        </main>
      </React.Fragment>
    );
  }
}

export default App;
