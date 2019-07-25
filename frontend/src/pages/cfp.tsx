import React, { useState } from "react";

import { Button, InputField, SelectField, TextareaField } from "fannypack";
import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomeLayout } from "../layouts/home";


type CfpProps = {
  data: any;
};

const ROW_PADDING = {
  mobile: 0.5,
  tabletPortrait: 0.5,
  tabletLandscape: 0.5,
  desktop: 1,
};

const BUTTON_PADDING = {
  mobile: 1,
  tabletPortrait: 1,
  tabletLandscape: 1,
  desktop: 2,
};

const ELEVATOR_PITCH_OPTIONS = [
  { label: "Sunny", value: "sunny" },
  { label: "Windy", value: "windy" },
  { label: "Overcast", value: "overcast" },
];

const TOPIC_OPTIONS = [
  { label: "PyWeb", value: "pyweb" },
  { label: "Python & Friends", value: "python_e_friends" },
  { label: "PyData", value: "pydata" },
];

const LANGUAGE_OPTIONS = [
  { label: "Italian", value: "ita" },
  { label: "English", value: "eng" },
];

const TYPE_OPTIONS = [
  { label: "Talk", value: "talk" },
  { label: "Training", value: "training" },
  { label: "Sprint", value: "sprint" },
];

const DURATION_OPTIONS = [
  { label: "2 hours", value: "2h" },
  { label: "45 minutes", value: "45m" },
  { label: "30 minutes", value: "30m" },
  { label: "5 minutes", value: "5m" },
];

const Form = () => {
  const [submission, setSubmission] = useState({
    title: "",
    abstract: "",
    elevatorPitch: "",
    topic: "",
    duration: "",
    language: "",
    type: "",
  });

  const sendSubmission = e => {
    console.log("lets send this submission!");
    console.dir(submission);
    // TODO ad me (user) to submission!
  };

  const onChangeForm = e => {
    const val = e.target.value;
    const name = e.target.id;
    console.log({ val, name });
    setSubmission(() => {
      return {
        ...submission,
        [name]: val,
      };
    });
  };

  return (

    <div>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <InputField a11yId="title" label="Title" value={submission.title} onChange={onChangeForm}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <TextareaField a11yId="abstract" label="Abstract" value={submission.abstract} onChange={onChangeForm}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <TextareaField a11yId="elevatorPitch" label="Elevator Pitch" value={submission.elevatorPitch}
                         onChange={onChangeForm} maxLength={300}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField a11yId="topic" label="Topic" value={submission.topic} onChange={onChangeForm}
                       options={TOPIC_OPTIONS}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField a11yId="language" label="Language" value={submission.language} onChange={onChangeForm}
                       options={LANGUAGE_OPTIONS}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField a11yId="type" label="type" value={submission.type} onChange={onChangeForm}
                       options={TYPE_OPTIONS}/>
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField a11yId="duration" label="Duration" value={submission.duration} onChange={onChangeForm}
                       options={DURATION_OPTIONS}/>
        </Container>
      </Row>


      <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
        <Container fullWidth={true}>
          <Button onClick={sendSubmission}>Send!</Button>
        </Container>
      </Row>

    </div>
  );
};

export default ({ data }: CfpProps) => (
  <HomeLayout>

    <Row paddingLeft={STANDARD_ROW_PADDING} paddingRight={STANDARD_ROW_PADDING}>
      <Column
        columnWidth={{
          mobile: 12,
          tabletPortrait: 12,
          tabletLandscape: 12,
          desktop: 8,
        }}
      >

        <Article hero={{ ...data.heroImage.childImageSharp }} title="Call For Proposal">
          {/*<Wrapper>*/}
          <Form/>
          {/*</Wrapper>*/}
        </Article>
      </Column>
    </Row>
  </HomeLayout>
);


export const query = graphql`
    query {
        heroImage: file(relativePath: { eq: "images/cfp.jpg" }) {
            childImageSharp {
                fluid(maxWidth: 1600) {
                    ...GatsbyImageSharpFluid
                }
            }
        }
    }
`;

