import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import {
  Alert,
  Button,
  Card,
  CheckboxField,
  FieldSet,
  FieldWrapper,
  Input,
  Radio,
  SelectField,
} from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React, { useCallback } from "react";
import { defineMessages, FormattedMessage, useIntl } from "react-intl";
import { useFormState } from "react-use-form-state";
import * as yup from "yup";

import { Form } from "../../components/form";
import { CountriesQuery } from "../../generated/graphql";
import {
  MyProfileQuery,
  UpdateMutation,
  UpdateMutationVariables,
} from "../../generated/graphql-backend";
import { BUTTON_PADDING, GENDER_COLUMN, ROW_PADDING } from "./constants";
import MY_PROFILE_QUERY from "./profile-edit.graphql";
import UPDATE_MUTATION from "./update.graphql";

type SectionWrapperProps = {
  titleId?: string;
  children: React.ReactNode;
};

const SectionWrapper = (props: SectionWrapperProps) => (
  <Card>
    <FieldSet>
      {props.titleId && (
        <h3>
          <FormattedMessage id={props.titleId} />
        </h3>
      )}
      {props.children}
    </FieldSet>
  </Card>
);

const schema = yup.object().shape({
  firstName: yup
    .string()
    .required()
    .ensure(),
  lastName: yup
    .string()
    .required()
    .ensure(),
  gender: yup
    .string()
    .required()
    .ensure(),
  dateBirth: yup.date(),
  country: yup
    .string()
    .required()
    .ensure(),
  openToRecruiting: yup.boolean(),
  openToNewsletter: yup.boolean(),
});

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

export const EditProfileApp: React.SFC<
  RouteComponentProps<{ lang: string }>
> = ({ lang }) => {
  const [formState, { text, radio, select, checkbox, raw }] = useFormState(
    {},
    {
      withIds: true,
    },
  );

  // region SETUP_OPTIONS
  const createOptions = (items: any[]) => [
    { label: "", value: "" },
    ...items.map(item => ({ label: item.name, value: item.id })),
  ];

  const {
    backend: { countries },
  } = useStaticQuery<CountriesQuery>(COUNTRIES_QUERY);
  const COUNTRIES_OPTIONS = createOptions(countries);

  const intl = useIntl();
  const genderMessages = defineMessages({
    male: {
      id: "profile.gender.male",
    },
    female: {
      id: "profile.gender.female",
    },
  });
  // endregion

  // region GET_USER_DATA
  const setProfile = (data: MyProfileQuery) => {
    const { me } = data;
    Object.keys(formState.values).forEach(field => {
      console.log(field, me[field]);
      formState.setField(field, me[field]);
    });
  };
  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY,
    { onCompleted: setProfile },
  );
  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }
  // endregion

  // region UPDATE_SEND_MUTATION

  const onUpdateComplete = (data: UpdateMutation) => {
    if (!data || data.update.__typename !== "MeUser") {
      Object.keys(formState.values).forEach(field => {
        const validationError = getValidationFieldError(
          data.update,
          field,
          "UpdateError",
        );
        formState.setFieldError(field, validationError);
      });

      return;
    }
    const profileUrl = `/${lang}/profile`;
    navigate(profileUrl);
  };

  const [update, { updateLoading, updateError, updateData }] = useMutation<
    UpdateMutation,
    UpdateMutationVariables
  >(UPDATE_MUTATION, {
    onCompleted: onUpdateComplete,
  });

  const onFormSubmit = useCallback(
    e => {
      e.preventDefault();

      schema
        .validate(formState.values, { abortEarly: false })
        .then(value => {
          formState.validity = {};
          formState.errors = {};

          console.log(
            "VALID! formState.values: " + JSON.stringify(formState.values),
          );
          update({
            variables: formState.values,
          });
        })
        .catch(err => {
          err.inner.forEach(item => {
            formState.setFieldError(item.path, item.message);
          });
        });
    },
    [update, formState],
  );

  const errorMessage =
    updateData && updateData.update.__typename === "UpdateErrors"
      ? updateData.update.nonFieldErrors.join(" ")
      : updateError;

  // endregion

  return (
    <>
      <h1>
        <FormattedMessage id="profile.header" />
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <Form onSubmit={onFormSubmit} method="post">
          {errorMessage && <Alert type="error">{errorMessage}</Alert>}

          <SectionWrapper titleId="profile.edit.personalHeader">
            <FieldWrapper
              validationText={formState.errors && formState.errors.firstName}
              state={
                formState.errors && formState.errors.firstName ? "danger" : ""
              }
              isRequired={true}
              label={
                <FormattedMessage id="profile.firstName">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input
                inputProps={{
                  id: "firstName",
                  ...text("firstName"),
                }}
                a11yId="firstName"
                isRequired={true}
              />
            </FieldWrapper>

            <FieldWrapper
              validationText={formState.errors && formState.errors.lastName}
              state={
                formState.errors && formState.errors.lastName ? "danger" : ""
              }
              isRequired={true}
              label={
                <FormattedMessage id="profile.lastName">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input
                inputProps={{
                  id: "lastName",
                  ...text("lastName"),
                }}
                a11yId="lastName"
              />
            </FieldWrapper>

            <FieldWrapper
              validationText={formState.errors && formState.errors.gender}
              state={
                formState.errors && formState.errors.gender ? "danger" : ""
              }
              isRequired={true}
              label={
                <FormattedMessage id="profile.gender">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <>
                <Row>
                  <Column columnWidth={GENDER_COLUMN}>
                    <Radio
                      {...radio("gender", "male")}
                      name="gender"
                      label={intl.formatMessage(genderMessages.male)}
                    />
                  </Column>
                  <Column columnWidth={GENDER_COLUMN}>
                    <Radio
                      {...radio("gender", "female")}
                      name="gender"
                      label={intl.formatMessage(genderMessages.female)}
                    />
                  </Column>
                </Row>
              </>
            </FieldWrapper>

            <FieldWrapper
              validationText={formState.errors && formState.errors.dateBirth}
              state={
                formState.errors && formState.errors.dateBirth ? "danger" : ""
              }
              isRequired={true}
              label={
                <FormattedMessage id="profile.dateBirth">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input
                {...raw({
                  name: "dateBirth",
                  onChange: event => {
                    const date = event.target.value;
                    formState.setField("dateBirth", new Date(date));
                    return date;
                  },
                })}
                type="date"
                a11yId="dateBirth"
              />
            </FieldWrapper>

            <FieldWrapper
              validationText={formState.errors && formState.errors.country}
              state={
                formState.errors && formState.errors.country ? "danger" : ""
              }
              isRequired={true}
              label={
                <FormattedMessage id="profile.country">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <SelectField
                {...select("country")}
                a11yId="country"
                options={COUNTRIES_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>
          </SectionWrapper>
          <br />
          <SectionWrapper titleId="profile.edit.privacyHeader">
            <FieldWrapper
              validationText={
                formState.errors && formState.errors.openToRecruiting
              }
              state={
                formState.errors && formState.errors.openToRecruiting
                  ? "danger"
                  : ""
              }
              label={<FormattedMessage id="profile.openToRecruiting" />}
            >
              <CheckboxField
                checkboxProps={{
                  id: "openToRecruiting",
                  ...checkbox("openToRecruiting"),
                }}
                type="checkbox"
              />
            </FieldWrapper>

            <FieldWrapper
              validationText={
                formState.errors && formState.errors.openToNewsletter
              }
              state={
                formState.errors && formState.errors.openToNewsletter
                  ? "danger"
                  : ""
              }
              label={<FormattedMessage id="profile.openToNewsletter" />}
            >
              <CheckboxField
                checkboxProps={{
                  id: "openToNewsletter",
                  ...checkbox("openToNewsletter"),
                }}
                type="checkbox"
              />
            </FieldWrapper>
          </SectionWrapper>
          <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
            <Button
              size="medium"
              palette="primary"
              isLoading={loading || updateLoading}
              type="submit"
            >
              <FormattedMessage id="buttons.save" />
            </Button>
          </Row>
        </Form>
      )}
    </>
  );
};

export const COUNTRIES_QUERY = graphql`
  query countries {
    backend {
      countries {
        code
        name
      }
    }
  }
`;
