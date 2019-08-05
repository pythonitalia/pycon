import React, { useState } from "react";

import { Button, InputField, Label, SelectField, TextareaField } from "fannypack";
import { graphql } from "gatsby";
import { Column, Container, Row } from "grigliata";
import * as yup from "yup";
import { Article } from "../components/article";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomeLayout } from "../layouts/home";


type CfpProps = {
  data: any;
};


const schema = yup.object().shape({
  title: yup.string().required().ensure(),
  elevatorPitch: yup.string(),
  abstract: yup.string().required().ensure(),
  topic: yup.string().required().ensure(),
  duration: yup.string().required().ensure(),
  language: yup.string().required().ensure(),
  type: yup.string().required().ensure(),
  audienceLevel: yup.string().required().ensure(),
});

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

const TOPIC_OPTIONS = [
  { label: "Select", value: "" },
  { label: "PyWeb", value: "pyweb" },
  { label: "Python & Friends", value: "python_e_friends" },
  { label: "PyData", value: "pydata" },
];

const LANGUAGE_OPTIONS = [
  { label: "English", value: "eng" },
  { label: "Italian", value: "ita" },
];

const TYPE_OPTIONS = [
  { label: "Select", value: "" },
  { label: "Talk", value: "talk" },
  { label: "Training", value: "training" },
  { label: "Sprint", value: "sprint" },
];

const DURATION_OPTIONS = [
  { label: "Select", value: "" },
  { label: "2 hours", value: "2h" },
  { label: "45 minutes", value: "45m" },
  { label: "30 minutes", value: "30m" },
  { label: "5 minutes", value: "5m" },
];

const AUDIENCE_LEVEL_OPTIONS = [
  { label: "Select", value: "" },
  { label: "Beginner", value: "beginner" },
  { label: "Intermidiate", value: "intermidiate" },
  { label: "Advanced", value: "advance" },
];

const Form = () => {
  const [errors, setErrors] = useState({});
  const [submission, setSubmission] = useState({
    title: "",
    abstract: "",
    elevatorPitch: "",
    topic: "",
    duration: "",
    language: "eng",
    type: "",
    audienceLevel: "",
  });

  const setFormsErrors = () => {

    schema.validate(submission, { abortEarly: false }).then(velue => {
      setErrors({});
    })
      .catch((err) => {
        const newErrors = {};
        err.inner.forEach(item => {
          newErrors[item.path] = item.message;
        });
        setErrors(newErrors);
    });
  };

  const handleSubmissionSubmit = (event) => {
    event.preventDefault();
    setFormsErrors();
    schema
      .isValid(submission)
      .then((valid) => {
        if (!valid) {
          console.log("Sorry submission has something wrong...");
          return;
        }
        console.log("The submission is Valid! Let's send now!");
        console.dir(submission);
        // TODO ad me (user) to submission!
      });
  };

  const hangleSubmissionChange = ({ target }) => {
    setSubmission(() => {
      return {
        ...submission,
        [target.id]: target.value,
      };
    });
  };

  return (

    <div>
      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <InputField
            a11yId="title"
            label="Title"
            value={submission.title}
            onChange={hangleSubmissionChange}
            isRequired={true}
            validationText={errors.title}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <TextareaField
            a11yId="abstract"
            label="Abstract"
            value={submission.abstract}
            onChange={hangleSubmissionChange}
            isRequired={true}
            validationText={errors.abstract}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <TextareaField
            a11yId="elevatorPitch"
            label="Elevator Pitch"
            value={submission.elevatorPitch}
            onChange={hangleSubmissionChange}
            maxLength={300}
            validationText={errors.elevatorPitch}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField
            a11yId="topic"
            label="Topic"
            value={submission.topic}
            onChange={hangleSubmissionChange}
            options={TOPIC_OPTIONS}
            isRequired={true}
            validationText={errors.topic}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField
            a11yId="language"
            label="Language"
            value={submission.language}
            onChange={hangleSubmissionChange}
            options={LANGUAGE_OPTIONS}
            isRequired={true}
            validationText={errors.language}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField
            a11yId="type"
            label="type"
            value={submission.type}
            onChange={hangleSubmissionChange}
            options={TYPE_OPTIONS}
            isRequired={true}
            validationText={errors.type}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField
            a11yId="duration"
            label="Duration"
            value={submission.duration}
            onChange={hangleSubmissionChange}
            options={DURATION_OPTIONS}
            isRequired={true}
            validationText={errors.duration}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING}>
        <Container fullWidth={true}>
          <SelectField
            a11yId="audienceLevel"
            label="Audience Level"
            value={submission.audienceLevel}
            onChange={hangleSubmissionChange}
            options={AUDIENCE_LEVEL_OPTIONS}
            isRequired={true}
            validationText={errors.audienceLevel}
          />
        </Container>
      </Row>

      <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
        <Container fullWidth={true}>
          <Button onClick={handleSubmissionSubmit}>Send!</Button>
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
          <Form/>
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
