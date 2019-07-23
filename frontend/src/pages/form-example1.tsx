import React from "react";

import Component from "@reactions/component";
import { Button, InputField } from "fannypack";
import { HomeLayout } from "../layouts/home";


export default class FormExample1 extends React.Component {
  state = {
    title: "my state title WOW!",
  };

  sendSubmission = (e) => {
    console.log("lets send this submission!");
    console.dir(this.state);
  }

  render() {
    return (
      <HomeLayout>
        <h1>Hello, {this.state.title}</h1>
        <Component initialState={{ title: "Fannypacks rock!" }}>
          {
            ({ state, setState }) =>
              <InputField a11yId="title" label="Title" onChange={e => setState({ title: e.target.value })}
                          value={state.title}/>
          }
        </Component>
        <Button onClick={this.sendSubmission}>Send!</Button>
      </HomeLayout>
    );
  }
}

