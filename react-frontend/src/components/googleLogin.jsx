import React, { Component } from "react";
import { GoogleLogin, GoogleLogout } from "react-google-login";

const googleClientLogin = process.env.REACT_APP_GOOGLE_CLIENT_ID;

class RenderGoogleAuth extends Component {
  state = {
    user: null
  };

  handleGoogleResponse = response => {
    try {
      var user = response.profileObj.name;
    } catch {
      user = null;
    }
    if (user !== null) {
      this.doGoogleLogin(response);
    } else {
      this.doGoogleLogout();
    }
  };

  doGoogleLogin = response => {
    console.log("store local storage");
    console.log("send api call to backend");
    const name = response.profileObj.name;
    this.setState({ user: name });
  };

  handleGoogleFailure = response => {
    console.log(response);
  };

  doGoogleLogout = () => {
    console.log("delete local storage");
    this.setState({ user: null });
  };

  render() {
    if (this.state.user === null) {
      return (
        <GoogleLogin
          clientId={googleClientLogin}
          onSuccess={this.handleGoogleResponse}
          onFailure={this.handleGoogleResponse}
          offline={false}
          approvalPrompt="force"
          responseType="id_token"
          isSignedIn
          theme="dark"
        />
      );
    } else {
      return (
        <GoogleLogout
          clientId={googleClientLogin}
          buttonText="Logout"
          onLogoutSuccess={this.handleGoogleResponse}
        />
      );
    }
  }
}

export default RenderGoogleAuth;
