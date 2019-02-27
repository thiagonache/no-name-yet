import React, { Component } from "react";
import Poll from "react-polls";
import { getVotes, incrementVotes } from "../services/pollService";

const pollQuestion1 = "Are you interested?";

class MainPoll extends Component {
  state = {
    pollAnswers1: [{ option: "Yes", votes: 0 }, { option: "No", votes: 0 }]
  };

  handleVote = (voteAnswer, pollAnswers, pollNumber) => {
    let total = 0;
    const newPollAnswers = pollAnswers.map(answer => {
      if (answer.option === voteAnswer) answer.votes++;
      total += answer.votes;

      return answer;
    });

    if (pollNumber === 1) {
      this.setState({
        pollAnswers1: newPollAnswers
      });
      try {
        incrementVotes(voteAnswer.toLowerCase());
      } catch (ex) {
        console.log(ex);
      }

      // } else {
      //   this.setState({
      //     pollAnswers2: newPollAnswers
      //   });
    }
  };

  async componentDidMount() {
    const { pollAnswers1 } = this.state;
    const { data: votesYes } = await getVotes("yes");
    const { data: votesNo } = await getVotes("no");
    const newPollAnswers = pollAnswers1.map(answer => {
      if (answer.option === "Yes") answer.votes = votesYes.votes;
      else if (answer.option === "No") answer.votes = votesNo.votes;
      return answer;
    });

    this.setState({
      pollAnswers1: newPollAnswers
    });
  }

  render() {
    const { pollAnswers1 } = this.state;
    return (
      <div>
        <Poll
          question={pollQuestion1}
          answers={pollAnswers1}
          onVote={voteAnswer => this.handleVote(voteAnswer, pollAnswers1, 1)}
        />
      </div>
    );
  }
}

export default MainPoll;
