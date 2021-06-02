import React, { Component } from "react";
import { render } from "react-dom";
import StarRating from "./StarRating";
import CommentList from "./CommentList";
import CommentForm from "./CommentForm";
import "./App.css";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <CommentForm />
        <CommentList />
      </div>
    );
  }
}

const appDiv = document.getElementById("comments");
// const name = document.getElementById("props").value;
render(<App />, appDiv);
