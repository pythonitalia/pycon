import React, { useState } from "react";

import { Button, InputField, SelectField, TextareaField } from "fannypack";
import { Column, Row } from "grigliata";
import * as yup from "yup";
import { AUDIENCE_LEVEL_OPTIONS, BUTTON_PADDING, DURATION_OPTIONS, LANGUAGE_OPTIONS, ROW_PADDING, TOPIC_OPTIONS, TYPE_OPTIONS } from "./constants";

const schema = yup.object().shape({
  title: yup
    .string()
    .required()
    .ensure(),
  elevatorPitch: yup.string(),
  abstract: yup
    .string()
    .required()
    .ensure(),
  topic: yup
    .string()
    .required()
    .ensure(),
  duration: yup
    .string()
    .required()
    .ensure(),
  language: yup
    .string()
    .required()
    .ensure(),
  type: yup
    .string()
    .required()
    .ensure(),
  audienceLevel: yup
    .string()
    .required()
    .ensure(),
});

const InputWrapper: React.FC = props => {
  return (
    <Row paddingBottom={ROW_PADDING}>
      <Column
        columnWidth={{
          mobile: 12,
          tabletPortrait: 12,
          tabletLandscape: 12,
          desktop: 12,
        }}
      >
        {props.children}
      </Column>
    </Row>
  );
};

export const CFPForm = () => {
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
    schema
      .validate(submission, { abortEarly: false })
      .then(velue => {
        setErrors({});
      })
      .catch(err => {
        const newErrors = {};
        err.inner.forEach(item => {
          newErrors[item.path] = item.message;
        });
        setErrors(newErrors);
      });
  };

  const handleSubmissionSubmit = event => {
    event.preventDefault();
    setFormsErrors();
    schema.isValid(submission).then(valid => {
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
      <InputWrapper>
        <InputField
          a11yId="title"
          label="Title"
          value={submission.title}
          onChange={hangleSubmissionChange}
          isRequired={true}
          validationText={errors.title}
        />
      </InputWrapper>

      <InputWrapper>
        <TextareaField
          a11yId="abstract"
          label="Abstract"
          value={submission.abstract}
          onChange={hangleSubmissionChange}
          isRequired={true}
          validationText={errors.abstract}
        />
      </InputWrapper>

      <InputWrapper>
        <TextareaField
          a11yId="elevatorPitch"
          label="Elevator Pitch"
          value={submission.elevatorPitch}
          onChange={hangleSubmissionChange}
          maxLength={300}
          validationText={errors.elevatorPitch}
        />
      </InputWrapper>

      <InputWrapper>
        <SelectField
          a11yId="topic"
          label="Topic"
          value={submission.topic}
          onChange={hangleSubmissionChange}
          options={TOPIC_OPTIONS}
          isRequired={true}
          validationText={errors.topic}
        />
      </InputWrapper>

      <InputWrapper>
        <SelectField
          a11yId="language"
          label="Language"
          value={submission.language}
          onChange={hangleSubmissionChange}
          options={LANGUAGE_OPTIONS}
          isRequired={true}
          validationText={errors.language}
        />
      </InputWrapper>

      <InputWrapper>
        <SelectField
          a11yId="type"
          label="type"
          value={submission.type}
          onChange={hangleSubmissionChange}
          options={TYPE_OPTIONS}
          isRequired={true}
          validationText={errors.type}
        />
      </InputWrapper>

      <InputWrapper>
        <SelectField
          a11yId="duration"
          label="Duration"
          value={submission.duration}
          onChange={hangleSubmissionChange}
          options={DURATION_OPTIONS}
          isRequired={true}
          validationText={errors.duration}
        />
      </InputWrapper>

      <InputWrapper>
        <SelectField
          a11yId="audienceLevel"
          label="Audience Level"
          value={submission.audienceLevel}
          onChange={hangleSubmissionChange}
          options={AUDIENCE_LEVEL_OPTIONS}
          isRequired={true}
          validationText={errors.audienceLevel}
        />
      </InputWrapper>

      <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
        <Button onClick={handleSubmissionSubmit}>Send!</Button>
      </Row>
    </div>
  );
};