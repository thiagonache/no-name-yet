import React from "react";

const Vote = props => {
  const previousAnswer = localStorage.getItem("pollAnswer");
  if (previousAnswer !== null) {
    return (
      <button
        className="btn btn-dark"
        onClick={props.onClick}
        aria-hidden="true"
        disabled
      >
        Vote
      </button>
    );
  } else {
    return (
      <button
        className="btn btn-info"
        onClick={props.onClick}
        style={{ cursor: "pointer" }}
        aria-hidden="true"
      >
        Vote
      </button>
    );
  }
};

export default Vote;
