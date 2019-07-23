import React from "react";

import Component from "@reactions/component";
import { Button, InputField } from "fannypack";
import { HomeLayout } from "../layouts/home";


export default class FormExampleWithoutHooks extends React.Component {
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
        <Component initialState={{ title: this.state.title }}>
          {
            ({ state, setState }) =>
              <InputField a11yId="title" label="Title" onChange={e => this.setState({ title: e.target.value })}
                          value={this.state.title}/>
          }
        </Component>
        <Button onClick={this.sendSubmission}>Send!</Button>
      </HomeLayout>
    );
  }
}

