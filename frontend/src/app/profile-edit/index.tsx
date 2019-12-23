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
  Select,
  Text,
} from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";
// @ts-ignore
import * as yup from "yup";

import { InputWrapper } from "../../components/input-wrapper";
import {
  MeUser,
  MyEditProfileQuery,
  UpdateProfileMutation,
  UpdateProfileMutationVariables,
} from "../../generated/graphql-backend";
import { useCountries } from "../../helpers/use-countries";
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
    <Box mb={5}>
      {titleId && (
        <Text mb={3} as="h3">
          <FormattedMessage id={titleId} />
        </Text>
      )}
      {children}
    </Box>
  </Card>
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

export const EditProfileApp: React.SFC<RouteComponentProps<{
  lang: string;
}>> = ({ lang }) => {
  const [formState, { text, select, checkbox, raw }] = useFormState<
    MeUserFields
  >(
    {},
    {
      withIds: true,
    },
  );

  const createOptions = (items: any[]) => [
    { label: "", value: "" },
    ...items.map(item => ({ label: item.name, value: item.id || item.code })),
  ];

  const countries = useCountries();

  const setUserFormFields = (me: MeUser) => {
    formState.setField("name", me.name ? me.name : "");
    formState.setField("fullName", me.fullName ? me.fullName : "");
    formState.setField("gender", me.gender ? me.gender : "");
    formState.setField(
      "dateBirth",
      me.dateBirth ? new Date(me.dateBirth) : new Date(),
    );
    formState.setField("country", me.country ? me.country : "");
    formState.setField(
      "openToRecruiting",
      me.openToRecruiting ? me.openToRecruiting : false,
    );
    formState.setField(
      "openToNewsletter",
      me.openToNewsletter ? me.openToNewsletter : false,
    );
  };

  // region GET_USER_DATA
  const setProfile = (profileData: MyEditProfileQuery) => {
    const { me } = profileData;
    setUserFormFields(me as MeUser);
  };
  const { loading, error } = useQuery<MyEditProfileQuery>(MY_PROFILE_QUERY, {
    onCompleted: setProfile,
  });
  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }
  // endregion

  // region UPDATE_SEND_MUTATION
  const onUpdateComplete = (data: UpdateProfileMutation) => {
    if (!data || data.update.__typename !== "MeUser") {
      return;
    }
    const profileUrl = `/${lang}/profile`;
    navigate(profileUrl);
  };
  const toTileCase = (word: string) =>
    word.charAt(0).toUpperCase() + word.slice(1);

  const getValidationError = (
    key:
      | "name"
      | "fullName"
      | "gender"
      | "dateBirth"
      | "country"
      | "openToRecruiting"
      | "openToNewsletter",
  ) => {
    const validationKey = "validation" + toTileCase(key);
    const validationError =
      (updateProfileData &&
        updateProfileData.update.__typename === "UpdateErrors" &&
        (updateProfileData.update as any)[validationKey].join(", ")) ||
      "";
    return validationError;
  };

  const [
    update,
    {
      loading: updateProfileLoading,
      error: updateProfileError,
      data: updateProfileData,
    },
  ] = useMutation<UpdateProfileMutation, UpdateProfileMutationVariables>(
    UPDATE_MUTATION,
    {
      onCompleted: onUpdateComplete,
    },
  );

  const onFormSubmit = useCallback(
    e => {
      e.preventDefault();

      schema
        .validate(formState.values, { abortEarly: false })
        .then(() => {
          formState.errors = {};

          update({
            variables: {
              name: formState.values.name,
              fullName: formState.values.fullName,
              gender: formState.values.gender,
              dateBirth: formState.values.dateBirth.toISOString().split("T")[0],
              country: formState.values.country,
              openToRecruiting: formState.values.openToRecruiting,
              openToNewsletter: formState.values.openToNewsletter,
            },
          });
        })
        .catch((err: { inner: any[] }) => {
          err.inner.forEach(item => {
            formState.setFieldError(item.path, item.message);
          });
        });
    },
    [update, formState],
  );

  const errorMessage =
    updateProfileData && updateProfileData.update.__typename === "UpdateErrors"
      ? updateProfileData.update.nonFieldErrors.join(" ")
      : updateProfileError;

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
      }}
    >
      <Text mb={4} as="h1">
        <FormattedMessage id="profile.header" />
      </Text>

      {loading && "Loading..."}
      {!loading && (
        <Box as="form" onSubmit={onFormSubmit}>
          {errorMessage && (
            <Alert mb={3} type="error">
              {errorMessage}
            </Alert>
          )}

          <SectionWrapper titleId="profile.edit.personalHeader">
            <InputWrapper
              errors={[formState.errors?.name || getValidationError("name")]}
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
              errors={[
                formState.errors?.fullName || getValidationError("fullName"),
              ]}
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
              errors={[
                formState.errors?.gender || getValidationError("gender"),
              ]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.gender">
                  {msg => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Select {...select("gender")}>
                <FormattedMessage id="profile.gender.selectGender">
                  {msg => <option value="">{msg}</option>}
                </FormattedMessage>
                <FormattedMessage id="profile.gender.male">
                  {msg => (
                    <option key="male" value="male">
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
                <FormattedMessage id="profile.gender.female">
                  {msg => (
                    <option key="female" value="female">
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
                <FormattedMessage id="profile.gender.other">
                  {msg => (
                    <option key="other" value="other">
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
                <FormattedMessage id="profile.gender.notSay">
                  {msg => (
                    <option key="notSay" value="not_say">
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
              </Select>
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.dateBirth || getValidationError("dateBirth"),
              ]}
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
                  onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
                    const timestamp = Date.parse(event.target.value);

                    if (!isNaN(timestamp)) {
                      const date = new Date(timestamp);
                      formState.setField("dateBirth", date);
                      return date;
                    }

                    return formState.values.dateBirth;
                  },
                })}
                value={
                  formState.values.dateBirth &&
                  formState.values.dateBirth.toISOString().split("T")[0]
                }
                type="date"
                required={true}
              />
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.country || getValidationError("country"),
              ]}
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
                {countries.map(c => (
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
              errors={[
                formState.errors?.openToRecruiting ||
                  getValidationError("openToRecruiting"),
              ]}
            >
              <Label>
                <Checkbox
                  {...checkbox("openToRecruiting")}
                  value={formState.values.openToRecruiting}
                />
                <FormattedMessage id="profile.openToRecruiting" />
              </Label>
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.openToNewsletter ||
                  getValidationError("openToNewsletter"),
              ]}
            >
              <Label>
                <Checkbox
                  {...checkbox("openToNewsletter")}
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
              isLoading={loading || updateProfileLoading}
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
