/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import {
  Alert,
  Box,
  Button,
  Card,
  Checkbox,
  Input,
  Label,
  Radio,
  Select,
  Text,
} from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import React, { useCallback } from "react";
import { defineMessages, FormattedMessage, useIntl } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Flex, jsx } from "theme-ui";
import * as yup from "yup";

import { CountriesQuery } from "../../generated/graphql";
import {
  MyProfileQuery,
  UpdateMutation,
  UpdateMutationVariables,
} from "../../generated/graphql-backend";
import MY_PROFILE_QUERY from "./profile-edit.graphql";
import UPDATE_MUTATION from "./update.graphql";

type MeUserFields = {
  name: string;
  fullName: string;
  gender: string;
  dateBirth: Date;
  country: string;
  openToRecruiting: boolean;
  openToNewsletter: boolean;
};

const SectionWrapper: React.SFC<{
  titleId?: string;
  children: React.ReactNode;
}> = ({ titleId, children }) => (
  <Card>
    <Box>
      {titleId && (
        <h3>
          <FormattedMessage id={titleId} />
        </h3>
      )}
      {children}
    </Box>
  </Card>
);

const InputWrapper: React.SFC<{
  label?: React.ReactElement;
  description?: React.ReactElement;
  error?: string;
  isRequired?: boolean;
}> = ({ label, error, isRequired, children }) => (
  <Box>
    {label && (
      <Text variant="profileEditLabel" as="p">
        {label}
      </Text>
    )}
    {children}
    {error && <Alert variant="alert">{error}</Alert>}
  </Box>
);

const schema = yup.object().shape({
  name: yup
    .string()
    .required()
    .ensure(),
  fullName: yup
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
  RouteComponentProps<{
    lang: string;
  }>
> = ({ lang }) => {
  const [formState, { text, radio, select, checkbox, raw }] = useFormState<
    MeUserFields
  >(
    {
      name: "",
      fullName: "",
    },
    {
      withIds: true,
    },
  );

  // region SETUP_OPTIONS
  const createOptions = (items: any[]) => [
    { label: "", value: "" },
    ...items.map(item => ({ label: item.name, value: item.id || item.code })),
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

  // @ts-ignore
  return (
    <Box>
      <h1>
        <FormattedMessage id="profile.header" />
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <Box as="form" onSubmit={onFormSubmit}>
          {errorMessage && <Alert type="error">{errorMessage}</Alert>}

          <SectionWrapper titleId="profile.edit.personalHeader">
            <InputWrapper
              error={formState.errors && formState.errors.name}
              isRequired={true}
              label={
                <FormattedMessage id="profile.name">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input {...text("name")} required={true} />
            </InputWrapper>

            <InputWrapper
              error={formState.errors && formState.errors.fullName}
              isRequired={true}
              label={
                <FormattedMessage id="profile.fullName">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input {...text("fullName")} required={true} />
            </InputWrapper>

            <InputWrapper
              error={formState.errors && formState.errors.gender}
              isRequired={true}
              label={
                <FormattedMessage id="profile.gender">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Flex>
                <Label>
                  <Radio {...radio("gender", "male")} name="gender" />
                  <FormattedMessage id="profile.gender.male" />
                </Label>
                <Label>
                  <Radio {...radio("gender", "female")} name="gender" />
                  <FormattedMessage id="profile.gender.female" />
                </Label>
              </Flex>
            </InputWrapper>

            <InputWrapper
              error={formState.errors && formState.errors.dateBirth}
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
                value={new Date(formState.values.dateBirth)}
                type="date"
                required={true}
              />
            </InputWrapper>

            <InputWrapper
              error={formState.errors && formState.errors.country}
              isRequired={true}
              label={
                <FormattedMessage id="profile.country">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Select
                {...select("country")}
                required={true}
                value={formState.values.country}
              >
                {COUNTRIES_OPTIONS.map(c => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </Select>
            </InputWrapper>
          </SectionWrapper>
          <br />
          <SectionWrapper titleId="profile.edit.privacyHeader">
            <InputWrapper
              error={formState.errors && formState.errors.openToRecruiting}
            >
              <Label>
                <Checkbox
                  checkboxProps={{
                    id: "openToRecruiting",
                    ...checkbox("openToRecruiting"),
                  }}
                  type="checkbox"
                  value={formState.values.openToRecruiting}
                />
                <FormattedMessage id="profile.openToRecruiting" />
              </Label>
            </InputWrapper>

            <InputWrapper
              error={formState.errors && formState.errors.openToNewsletter}
            >
              <Label>
                <Checkbox
                  checkboxProps={{
                    id: "openToNewsletter",
                    ...checkbox("openToNewsletter"),
                  }}
                  type="checkbox"
                  value={formState.values.openToNewsletter}
                />
                <FormattedMessage id="profile.openToNewsletter" />
              </Label>
            </InputWrapper>
          </SectionWrapper>
          <Box>
            <Button
              size="medium"
              palette="primary"
              isLoading={loading || updateLoading}
              type="submit"
            >
              <FormattedMessage id="buttons.save" />
            </Button>
          </Box>
        </Box>
      )}
    </Box>
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
