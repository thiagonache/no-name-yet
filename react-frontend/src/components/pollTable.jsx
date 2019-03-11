import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import auth from "../services/authService";
import Table from "./common/table";
import Vote from "./vote";

class PollTable extends Component {
  constructor() {
    super();
    const user = auth.getCurrentUser();
    if (user && user.isAdmin) this.columns.push(this.deleteColumn);
  }

  renderCheck = answer => {
    const myAnswer = localStorage.getItem("pollAnswer");
    if (answer === myAnswer) {
      return <FontAwesomeIcon icon={faCheck} />;
    }
  };

  columns = [
    {
      path: "id",
      key: "vote",
      content: answer => (
        <Vote
          answer={answer.voted}
          onClick={() => this.props.onVoteIncrement(answer.description)}
        />
      )
    },
    {
      path: "description",
      label: "Answer"
    },
    { path: "votes", label: "Votes" },
    { path: "created_by", label: "Added by" },
    {
      path: "",
      key: "check",
      content: answer => this.renderCheck(answer.description)
    }
  ];

  deleteColumn = {
    key: "delete",
    content: movie => (
      <button
        onClick={() => this.props.onDelete(movie)}
        className="btn btn-danger btn-sm"
      >
        Delete
      </button>
    )
  };

  render() {
    const { pollAnswers, onSort, sortColumn, incrementVotes } = this.props;
    return (
      <Table
        columns={this.columns}
        data={pollAnswers}
        sortColumn={sortColumn}
        onSort={onSort}
        onClick={incrementVotes}
      />
    );
  }
}

export default PollTable;
