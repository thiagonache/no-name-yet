import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
import { saveAnswer } from "../services/pollService";

class AnswerForm extends Form {
  state = {
    data: { answer: "" },
    errors: {}
  };

  schema = {
    answer: Joi.string()
      .required()
      .label("Answer")
  };

  doSubmit = async () => {
    const { data } = this.state;
    try {
      await saveAnswer(data.answer);
      window.location = "/poll";
    } catch (ex) {
      console.log(ex);
    }
  };

  render() {
    return (
      <div className="m-4 d-flex justify-content-left">
        <form onSubmit={this.handleSubmit}>
          {this.renderInput("answer", "")}
          {this.renderButton("Add new")}
        </form>
      </div>
    );
  }
}

export default AnswerForm;
