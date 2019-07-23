import React, { useState } from "react";

import Component from "@reactions/component";
import { Button, InputField } from "fannypack";
import { HomeLayout } from "../layouts/home";

type CfpProps = {
  data: any;
};


export default ({ data }: CfpProps) => {
  const [submission, setSubmission] = useState({
    title: "My initial Title!! Yey!",
    abstract: "My initial Abstract",
  });

  const sendSubmission = (e) => {
    console.log("lets send this submission!");
    console.dir(submission);
  };

    return(
  <HomeLayout>
    <Component initialState={{ title: submission.title }}>
      {
        ({ state, setState }) =>
          <InputField a11yId="title" label="Title" value={submission.title} onChange={e => {
            const val = e.target.value;
            setSubmission(prevState => {
              return { ...prevState, title: val };
            });
          }}
          />

      }
    </Component>


    <Component initialState={{ abstract: submission.abstract }}>
      {
        ({ state, setState }) =>
          <InputField a11yId="abstract" label="Abstract"  value={submission.abstract} onChange={e => {
            const val = e.target.value;
            setSubmission(prevState => {
              return { ...prevState, abstract: val };
            });
          }}/>

      }
    </Component>

    <Button onClick={sendSubmission}>Send!</Button>
  </HomeLayout>
);

};
