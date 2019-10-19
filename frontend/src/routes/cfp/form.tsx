import {
  Button,
  FieldSet,
  FieldWrapper,
  Input,
  Label,
  Select,
  Textarea,
} from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import * as yup from "yup";

import { Form } from "../../components/form";
import { BUTTON_PADDING, ROW_PADDING, TYPE_OPTIONS } from "./constants";

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

const InputWrapper: React.FC = props => (
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

export const constantsQuery = graphql`
  query Constants {
    backend {
      conference {
        topics {
          id
          name
        }
        durations {
          id
          name
        }
        audienceLevels {
          id
          name
        }
        languages {
          id
          name
        }
      }
    }
  }
`;

const createOptions = (items: any[]) => [
  { label: "", value: "" },
  ...items.map(item => ({ label: item.name, value: item.id })),
];

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

  const data = useStaticQuery(constantsQuery);

  const {
    backend: {
      conference: { topics, durations, audienceLevels, languages },
    },
  } = data;

  const TOPIC_OPTIONS = createOptions(topics);
  const DURATION_OPTIONS = createOptions(durations);
  const LANGUAGE_OPTIONS = createOptions(languages);
  const AUDIENCE_LEVEL_OPTIONS = createOptions(audienceLevels);

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

  // TODO: types
  const [formState, { label, select, text, textarea }] = useFormState(
    {},
    {
      withIds: true,
    },
  );

  return (
    <Form
      method="post"
      onSubmit={e => {
        e.preventDefault();
      }}
    >
      <FieldSet>
        <FieldWrapper
          label={
            <Label {...label("title")}>
              <FormattedMessage id="cfp.form.title" />
            </Label>
          }
        >
          <Input
            inputProps={{ ...text("title"), required: true }}
            isRequired={true}
          />
        </FieldWrapper>

        <FieldWrapper
          label={
            <Label {...label("abstract")}>
              <FormattedMessage id="cfp.form.abstract" />
            </Label>
          }
        >
          <Textarea {...textarea("abstract")} isRequired={true} />
        </FieldWrapper>

        <FieldWrapper
          label={
            <Label {...label("elevatorPitch")}>
              <FormattedMessage id="cfp.form.elevatorPitch" />
            </Label>
          }
          description={
            <FormattedMessage id="cfp.form.elevatorPitch.description" />
          }
        >
          <Textarea {...textarea("elevatorPitch")} isRequired={true} />
        </FieldWrapper>

        {/* TODO: multiple languages */}
        <Label {...label("language")}>
          <FormattedMessage id="cfp.form.language" />
        </Label>
        <Select
          {...select("language")}
          options={LANGUAGE_OPTIONS}
          isRequired={true}
        />

        <Label {...label("topic")}>
          <FormattedMessage id="cfp.form.topic" />
        </Label>
        <Select
          {...select("topic")}
          options={TOPIC_OPTIONS}
          isRequired={true}
        />

        <Label {...label("submissionType")}>
          <FormattedMessage id="cfp.form.submissionType" />
        </Label>
        <Select
          {...select("submissionType")}
          options={TYPE_OPTIONS}
          isRequired={true}
        />

        <Label {...label("duration")}>
          <FormattedMessage id="cfp.form.duration" />
        </Label>
        <Select
          {...select("duration")}
          options={DURATION_OPTIONS}
          isRequired={true}
        />

        <Label {...label("audienceLevel")}>
          <FormattedMessage id="cfp.form.audienceLevel" />
        </Label>
        <Select
          {...select("audienceLevel")}
          options={AUDIENCE_LEVEL_OPTIONS}
          isRequired={true}
        />

        <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
          <Button size="medium" palette="primary" type="submit">
            <FormattedMessage id="cfp.form.sendSubmission" />
          </Button>
        </Row>
      </FieldSet>
    </Form>
  );
};
