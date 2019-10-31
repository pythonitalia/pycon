import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import {
  Alert,
  Button,
  Card,
  CheckboxField,
  FieldWrapper,
  Input,
  RadioGroupField,
  SelectField,
  FieldSet,
} from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { Form } from "../../components/form";
import { CountriesQuery } from "../../generated/graphql";
import { MyProfileQuery, UpdateMutation, UpdateMutationVariables } from "../../generated/graphql-backend";
import { BUTTON_PADDING, COLUMN_WIDTH, ROW_PADDING } from "./constants";
import MY_PROFILE_QUERY from "./profile-edit.graphql";
import UPDATE_MUTATION from "./update.graphql";

type SectionWrapperProps = {
  titleId?: string;
  children: React.ReactNode
};

const SectionWrapper = (props: SectionWrapperProps) => {
  return (
    <Card>
      <FieldSet>
        {
          props.titleId &&
          <h3>
            <FormattedMessage id={props.titleId}/>
          </h3>
        }
        {props.children}
      </FieldSet>
    </Card>
  )
};

const FORM_FIELDS = [
  "firstName",
  "lastName",
  "gender",
  "dateBirth",
  "country",
  "openToRecruiting",
  "openToNewsletter",
];

export const EditProfileApp: React.SFC<RouteComponentProps<{ lang: string }>> = ({
                                                                                   lang,
                                                                                 }) => {
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
  // endregion

  // region GET_USER_DATA
  const setProfile = (data: MyProfileQuery) => {
    const { me } = data;
    FORM_FIELDS.forEach(field => formState.setField(field, me[field]));
    formState.setField("dateBirth", me.dateBirth ? me.dateBirth : "");
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
      return;
    }
    const profileUrl = `/${lang}/profile`;
    navigate(profileUrl);
  };

  const [update, { updateLoading, updateError, updateData }] = useMutation<UpdateMutation,
    UpdateMutationVariables>(UPDATE_MUTATION, {
    onCompleted: onUpdateComplete,
  });

  const onFormSubmit = useCallback(
    e => {
      e.preventDefault();
      console.log(
        "onFormSubmit! formState.values: " + JSON.stringify(formState.values),
      );
      update({
        variables: formState.values,
      });
    },
    [update, formState],
  );

  // region GET_ERRORS
  const errorMessage =
    updateData && updateData.update.__typename === "UpdateErrors"
      ? updateData.update.nonFieldErrors.join(" ")
      : updateError;

  const getFieldError = field =>
    (updateData &&
      updateData.update.__typename === "UpdateErrors" &&
      updateData.update[field].join(", ")) ||
    "";

  const toTileCase = word => word.charAt(0).toUpperCase() + word.slice(1);

  const errorsFields = {};
  FORM_FIELDS.forEach(field => {
    const validationField = "validation" + toTileCase(field);
    errorsFields[field] = getFieldError(validationField);
  });
  // endregion

  // endregion

  return (
    <>
      <h1>
        <FormattedMessage id="profile.header"/>
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <Form onSubmit={onFormSubmit} method="post">

          {errorMessage && <Alert type="error">{errorMessage}</Alert>}

          <SectionWrapper titleId="profile.edit.personalHeader">
            <FieldWrapper
              validationText={errorsFields.firstaName}
              state={errorsFields.firstName ? "danger" : ""}
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

            <FieldWrapper validationText={errorsFields.lastName}
                          state={errorsFields.lastName ? "danger" : ""} isRequired={true}
                          label={
                            <FormattedMessage id="profile.lastName">
                              {msg => <b>{msg}</b>}
                            </FormattedMessage>
                          }>
              <Input
                inputProps={{
                  id: "lastName",
                  ...text("lastName"),
                }}
                a11yId="lastName"
              />
            </FieldWrapper>

            <FieldWrapper validationText={errorsFields.gender}
                          state={errorsFields.gender ? "danger" : ""} isRequired={true}
                          label={
                            <FormattedMessage id="profile.gender">
                              {msg => <b>{msg}</b>}
                            </FormattedMessage>
                          }>
              <RadioGroupField
                {...radio("gender")}
                isHorizontal={true}
                a11yId="gender"
                options={[
                  { label: "Male", value: "male" },
                  { label: "Female", value: "female" },
                ]}
              />
            </FieldWrapper>

            <FieldWrapper validationText={errorsFields.dateBirth}
                          state={errorsFields.dateBirth ? "danger" : ""} isRequired={true}
                          label={
                            <FormattedMessage id="profile.dateBirth">
                              {msg => <b>{msg}</b>}
                            </FormattedMessage>
                          }>
              <Input
                {...raw("dateBirth")}
                type="date"
                a11yId="dateBirth"
              />
            </FieldWrapper>

            <FieldWrapper validationText={errorsFields.country}
                          state={errorsFields.country ? "danger" : ""} isRequired={true}
                          label={
                            <FormattedMessage id="profile.country">
                              {msg => <b>{msg}</b>}
                            </FormattedMessage>
                          }>
              <SelectField
                {...select("country")}
                a11yId="country"
                options={COUNTRIES_OPTIONS}
                isRequired={true}
              />
            </FieldWrapper>
          </SectionWrapper>
          <br/>
          <SectionWrapper titleId="profile.edit.privacyHeader">
            <FieldWrapper validationText={errorsFields.openToRecruiting}
                          state={errorsFields.openToRecruiting ? "danger" : ""}
                          label={<FormattedMessage id="profile.openToRecruiting"/>} >
              <CheckboxField
                checkboxProps={{
                  id: "openToRecruiting",
                  ...checkbox("openToRecruiting"),
                }}
                type="checkbox"
              />
            </FieldWrapper>

            <FieldWrapper validationText={errorsFields.openToNewsletter}
                                state={errorsFields.openToNewsletter ? "danger" : ""}
                                label={<FormattedMessage id="profile.openToNewsletter"/>}>
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
              isLoading={loading}
              type="submit"
            >
              <FormattedMessage id="buttons.save"/>
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
