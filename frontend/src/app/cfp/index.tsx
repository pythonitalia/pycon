import { RouteComponentProps } from "@reach/router";
import * as React from "react";
import { graphql, useStaticQuery } from "gatsby";
import { Article } from "../../components/article";
import { Form } from "../../components/form";
import {
  Button,
  FieldSet,
  FieldWrapper,
  Input,
  Label,
  Select,
  Textarea,
} from "fannypack";
import { FormattedMessage } from "react-intl";
import { BUTTON_PADDING, ROW_PADDING, TYPE_OPTIONS } from "./constants";
import { Row } from "grigliata";
import { useFormState } from "react-use-form-state";
import * as yup from "yup";

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
  submissionType: yup
    .string()
    .required()
    .ensure(),
  audienceLevel: yup
    .string()
    .required()
    .ensure(),
});

const createOptions = (items: any[]) => [
  { label: "", value: "" },
  ...items.map(item => ({ label: item.name, value: item.id })),
];

export const CfpForm: React.SFC<RouteComponentProps> = () => {
  const [formState, { label, select, text, textarea }] = useFormState(
    {},
    {
      withIds: true,
    },
  );

  // region SETUP_CONSTANTS
  const {
    heroImage,
    backend: {
      conference: { topics, durations, audienceLevels, languages },
    },
  } = useStaticQuery(query);
  const TOPIC_OPTIONS = createOptions(topics);
  const DURATION_OPTIONS = createOptions(durations);
  const LANGUAGE_OPTIONS = createOptions(languages);
  const AUDIENCE_LEVEL_OPTIONS = createOptions(audienceLevels);
  // TODO SubmissionTypes options from BE!
  // endregion

  // region ERRORS
  const setFormsErrors = () => {
    schema
      .validate(formState.values, { abortEarly: false })
      .then(value => {
        formState.validity = {};
        formState.errors = {};
        console.log("wooow it's valid!!");
      })
      .catch(err => {
        const newErrors = {};
        err.inner.forEach(item => {
          formState.setFieldError(item.path, item.message);
        });
      });
  };
  // endregion

  return (
    <>
      <Article
        hero={{ ...heroImage!.childImageSharp }}
        title="Call For Proposal"
      >
        <Form
          method="post"
          onSubmit={e => {
            e.preventDefault();
            setFormsErrors();
          }}
        >
          <FieldSet>
            <FieldWrapper
              label={
                <Label {...label("title")}>
                  <FormattedMessage id="cfp.form.title" />
                </Label>
              }
              isRequired={true}
              validationText={formState.errors && formState.errors.title}
              state={formState.errors && formState.errors.title ? "danger" : ""}
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
              isRequired={true}
              validationText={formState.errors && formState.errors.abstract}
              state={
                formState.errors && formState.errors.abstract ? "danger" : ""
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
              validationText={
                formState.errors && formState.errors.elevatorPitch
              }
              state={
                formState.errors && formState.errors.elevatorPitch
                  ? "danger"
                  : ""
              }
            >
              <Textarea {...textarea("elevatorPitch")} isRequired={true} />
            </FieldWrapper>

            {/* TODO: multiple languages */}

            <FieldWrapper
              label={
                <Label {...label("language")}>
                  <FormattedMessage id="cfp.form.language" />
                </Label>
              }
              isRequired={true}
              validationText={formState.errors && formState.errors.language}
              state={
                formState.errors && formState.errors.language ? "danger" : ""
              }
            >
              <Select
                {...select("language")}
                options={LANGUAGE_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>

            <FieldWrapper
              label={
                <Label {...label("topic")}>
                  <FormattedMessage id="cfp.form.topic" />
                </Label>
              }
              isRequired={true}
              validationText={formState.errors && formState.errors.topic}
              state={formState.errors && formState.errors.topic ? "danger" : ""}
            >
              <Select
                {...select("topic")}
                options={TOPIC_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>

            <FieldWrapper
              label={
                <Label {...label("submissionType")}>
                  <FormattedMessage id="cfp.form.submissionType" />
                </Label>
              }
              isRequired={true}
              validationText={
                formState.errors && formState.errors.submissionType
              }
              state={
                formState.errors && formState.errors.submissionType
                  ? "danger"
                  : ""
              }
            >
              <Select
                {...select("submissionType")}
                options={TYPE_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>

            <FieldWrapper
              label={
                <Label {...label("duration")}>
                  <FormattedMessage id="cfp.form.duration" />
                </Label>
              }
              isRequired={true}
              validationText={formState.errors && formState.errors.duration}
              state={
                formState.validity && formState.validity.duration === false
                  ? "danger"
                  : ""
              }
            >
              <Select
                {...select("duration")}
                options={DURATION_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>

            <FieldWrapper
              label={
                <Label {...label("audienceLevel")}>
                  <FormattedMessage id="cfp.form.audienceLevel" />
                </Label>
              }
              isRequired={true}
              validationText={
                formState.errors && formState.errors.audienceLevel
              }
              state={
                formState.validity && formState.validity.audienceLevel === false
                  ? "danger"
                  : ""
              }
            >
              <Select
                {...select("audienceLevel")}
                options={AUDIENCE_LEVEL_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>

            <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
              <Button size="medium" palette="primary" type="submit">
                <FormattedMessage id="cfp.form.sendSubmission" />
              </Button>
            </Row>
          </FieldSet>
        </Form>
      </Article>
    </>
  );
};

const query = graphql`
  query CFP {
    heroImage: file(relativePath: { eq: "images/cfp.jpg" }) {
      childImageSharp {
        fluid(
          maxWidth: 1600
          maxHeight: 700
          fit: COVER
          cropFocus: ATTENTION
          duotone: { highlight: "#000000", shadow: "#000000", opacity: 20 }
        ) {
          ...GatsbyImageSharpFluid
        }
      }
    }
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
