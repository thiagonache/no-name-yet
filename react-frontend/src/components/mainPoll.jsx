import React, { Component } from "react";
import _ from "lodash";
import { getAnswers, getPolls, incrementVotes } from "../services/pollService";
import AnswerForm from "./answerForm";
import PollTable from "./pollTable";

class MainPoll extends Component {
  state = {
    pollQuestion: "",
    pollAnswers: [],
    sortColumn: { path: "description", order: "asc" }
  };

  async componentDidMount() {
    const { data: answers } = await getAnswers();
    const { data: polls } = await getPolls();
    let total = 0;

    answers["items"].map(item => {
      total += item.votes;
      return total;
    });

    this.setState({
      pollAnswers: answers.items,
      pollQuestion: polls.items[0]["name"],
      total: total
    });
  }

  handleVote = voteAnswer => {
    const { pollAnswers } = this.state;
    let total = 0;
    const newPollAnswers = pollAnswers.map(answer => {
      if (answer.description === voteAnswer) answer.votes++;
      total += answer.votes;
      return answer;
    });

    try {
      incrementVotes(voteAnswer);
    } catch (ex) {
      console.log(ex);
    }

    this.setState({
      pollAnswers: newPollAnswers,
      total: total
    });
  };

  handleSort = sortColumn => {
    this.setState({ sortColumn });
  };

  render() {
    const { pollAnswers, pollQuestion, total, sortColumn } = this.state;
    const sorted = _.orderBy(
      pollAnswers,
      [sortColumn.path],
      [sortColumn.order]
    );

    return (
      <React.Fragment>
        {this.props.user === null && (
          <div className="alert alert-dark my-lg-0 " role="alert">
            Log in to be able to add new answers. The vote is anonymous.
          </div>
        )}
        {this.props.user !== null && <AnswerForm question={pollQuestion} />}
        <div className="m-4 d-flex justify-content-center">
          <h2>{pollQuestion}</h2>
        </div>
        <div className="m-4 d-flex justify-content-center">
          <PollTable
            pollAnswers={sorted}
            sortColumn={sortColumn}
            onSort={this.handleSort}
            onVoteIncrement={this.handleVote}
          />
        </div>
        <div className="m-4 d-flex justify-content-center">
          Total votes: {total}
        </div>
      </React.Fragment>
    );
  }
}

export default MainPoll;
