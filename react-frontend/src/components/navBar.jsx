import React from "react";
import { NavLink } from "react-router-dom";

const NavBar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="collapse navbar-collapse" id="navbarText">
        <ul className="navbar-nav mr-auto">
          <li className="nav-item">
            <NavLink className="nav-link" to="/home">
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/features">
              Features
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/architecture">
              Architecture
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/poll">
              Poll
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink className="nav-link" to="/about">
              About
            </NavLink>
          </li>
        </ul>
        <span className="navbar-text">
          <a href="https://github.com/thiagonache/no-name-yet" target="_blank">
            Source code
          </a>
        </span>
      </div>
    </nav>
  );
};

export default NavBar;
