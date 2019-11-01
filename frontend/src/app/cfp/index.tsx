import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import {
  Alert,
  Button,
  FieldSet,
  FieldWrapper,
  Input,
  Label,
  Select,
  Textarea,
} from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import { Row } from "grigliata";
import * as React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import * as yup from "yup";

import { Article } from "../../components/article";
import { Form } from "../../components/form";
import {
  SendSubmissionMutation,
  SendSubmissionMutationVariables,
} from "../../generated/graphql-backend";
import { CfpOpenCheck } from "./cfp-open-check";
import { BUTTON_PADDING, ROW_PADDING } from "./constants";
import SEND_SUBMISSION_MUTATION from "./sendSubmission.graphql";

const schema = yup.object().shape({
  title: yup
    .string()
    .required()
    .ensure(),
  elevatorPitch: yup.string().max(300),
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

const createOptions = (items: any[]) => [
  { label: "", value: "" },
  ...items.map(item => ({
    label: item.name,
    value: item.id || item.code || item.name,
  })),
];

const toTileCase = (word: string) =>
  word.charAt(0).toUpperCase() + word.slice(1);

// TODO put this in a "utils" module...
const getValidationFieldError = (
  data: any,
  field: string,
  typename: string,
) => {
  const errorType = "validation" + toTileCase(field);
  const validationError =
    (data.__typename === typename &&
      data[errorType] &&
      data[errorType].join(", ")) ||
    "";
  return validationError;
};

const getUniqueObjects = data => {
  const uniqueItems = {};
  data.forEach(item => (uniqueItems[item.id] = item));
  return Object.values(uniqueItems);
};

export const CfpForm: React.SFC<RouteComponentProps> = () => {
  const [formState, { label, select, text, textarea }] = useFormState(
    {},
    {
      withIds: true,
    },
  );

  const {
    heroImage,
    backend: {
      conference: { topics, durations, audienceLevels, languages },
    },
  } = useStaticQuery(query);

  const getAllowedSubmissionTypesOptions = (
    durationsList,
    durationSelected?: string,
  ) => {
    console.log(durations, durationSelected);
    let durationsSelcted = durationsList;
    if (durationSelected) {
      durationsSelcted = durationsList.filter(
        item => item.id === durationSelected,
      );
    }

    const submissionTypes = [].concat(
      ...durationsSelcted.map(
        duration => duration.allowedSubmissionTypes || [],
      ),
    );
    const uniqueSubmissionTypes = getUniqueObjects(submissionTypes);
    console.log(uniqueSubmissionTypes);
    return createOptions(uniqueSubmissionTypes);
  };

  const TOPIC_OPTIONS = createOptions(topics);
  const DURATION_OPTIONS = createOptions(durations);
  const LANGUAGE_OPTIONS = createOptions(languages);
  const AUDIENCE_LEVEL_OPTIONS = createOptions(audienceLevels);
  // region ON_SUBMIT

  const onSendSubmissionComplete = (
    sendSubmissionData: SendSubmissionMutation,
  ) => {
    if (
      !sendSubmissionData ||
      sendSubmissionData.sendSubmission.__typename !== "Submission"
    ) {
      Object.keys(formState.values).forEach(field => {
        const errorField = getValidationFieldError(
          sendSubmissionData.sendSubmission,
          field,
          "SendSubmissionErrors",
        );
        formState.setFieldError(field, errorField);
      });
      return;
    }
  };

  const [sendSubmission, { loading, error, data }] = useMutation<
    SendSubmissionMutation,
    SendSubmissionMutationVariables
  >(SEND_SUBMISSION_MUTATION, {
    onCompleted: onSendSubmissionComplete,
  });

  const setFormsErrors = () => {
    schema
      .validate(formState.values, { abortEarly: false })
      .then(value => {
        formState.validity = {};
        formState.errors = {};

        const variables = formState.values;
        variables.conference = "pycon-demo";
        sendSubmission({
          variables,
        });
      })
      .catch(err => {
        const newErrors = {};
        err.inner.forEach(item => {
          formState.setFieldError(item.path, item.message);
        });
      });
  };
  // endregion

  const errorMessage =
    data && data.sendSubmission.__typename === "SendSubmissionErrors"
      ? data.sendSubmission.nonFieldErrors.join(" ")
      : error;

  const successSendMutation =
    data && data.sendSubmission.__typename === "Submission";

  return (
    <>
      <Article
        hero={{ ...heroImage!.childImageSharp }}
        title="Call For Proposal"
      >
        <CfpOpenCheck>
          <Form
            method="post"
            onSubmit={e => {
              e.preventDefault();
              setFormsErrors();
            }}
          >
            {errorMessage && <Alert type="danger">{errorMessage}</Alert>}
            {successSendMutation && (
              <Alert type="success">
                <FormattedMessage id="cfp.form.messages.sendSubmissionSuccess" />
              </Alert>
            )}
            <br />
            <FieldSet>
              <FieldWrapper
                label={
                  <Label {...label("title")}>
                    <FormattedMessage id="cfp.form.title" />
                  </Label>
                }
                isRequired={true}
                validationText={formState.errors && formState.errors.title}
                state={
                  formState.errors && formState.errors.title ? "danger" : ""
                }
              >
                <Input
                  inputProps={{ ...text("title"), required: true }}
                  isRequired={true}
                  disabled={successSendMutation}
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
                <Textarea
                  {...textarea("abstract")}
                  isRequired={true}
                  disabled={successSendMutation}
                />
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
                <Textarea
                  {...textarea("elevatorPitch")}
                  isRequired={true}
                  disabled={successSendMutation}
                />
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
                  disabled={successSendMutation}
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
                state={
                  formState.errors && formState.errors.topic ? "danger" : ""
                }
              >
                <Select
                  {...select("topic")}
                  options={TOPIC_OPTIONS}
                  isRequired={true}
                  disabled={successSendMutation}
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
                  formState.validity && formState.errors.duration
                    ? "danger"
                    : ""
                }
              >
                <Select
                  {...select("duration")}
                  options={DURATION_OPTIONS}
                  isRequired={true}
                  disabled={successSendMutation}
                />
              </FieldWrapper>

              <FieldWrapper
                label={
                  <Label {...label("type")}>
                    <FormattedMessage id="cfp.form.type" />
                  </Label>
                }
                isRequired={true}
                validationText={formState.errors && formState.errors.type}
                state={
                  formState.errors && formState.errors.type ? "danger" : ""
                }
              >
                <Select
                  {...select("type")}
                  options={getAllowedSubmissionTypesOptions(
                    durations,
                    formState.values.duration,
                  )}
                  isRequired={true}
                  disabled={successSendMutation}
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
                  formState.errors && formState.errors.audienceLevel
                    ? "danger"
                    : ""
                }
              >
                <Select
                  {...select("audienceLevel")}
                  options={AUDIENCE_LEVEL_OPTIONS}
                  isRequired={true}
                  disabled={successSendMutation}
                />
              </FieldWrapper>

              <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
                <Button
                  size="medium"
                  palette="primary"
                  type="submit"
                  isLoading={loading}
                  disabled={successSendMutation}
                >
                  <FormattedMessage id="cfp.form.sendSubmission" />
                </Button>
              </Row>
            </FieldSet>
          </Form>
        </CfpOpenCheck>
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
          allowedSubmissionTypes {
            name
          }
        }
        audienceLevels {
          name
        }
        languages {
          code
          name
        }
      }
    }
  }
`;
