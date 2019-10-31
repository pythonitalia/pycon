import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import {
  Alert,
  Button,
  Card,
  CheckboxField,
  FieldWrapper,
  InputField,
  LayoutSet,
  RadioGroupField,
  SelectField,
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

type InputWrapperProps = {
  text: string;
  isRequired: boolean;
};

const InputWrapper: React.FC = (props: InputWrapperProps) => (
  <Row paddingBottom={ROW_PADDING}>
    <Column
      columnWidth={{
        mobile: 12,
        tabletPortrait: 12,
        tabletLandscape: 12,
        desktop: 12,
      }}
    >
      <FieldWrapper
        validationText={props.text}
        state={props.text ? "danger" : ""}
        isRequired={props.isRequired}
      >
        {props.children}
      </FieldWrapper>
    </Column>
  </Row>
);

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

  useEffect(() => {
    // Update the document title using the browser API
    console.log(
      "Effect: formState.values: " + JSON.stringify(formState.values),
    );
  });

  return (
    <>
      <h1>
        <FormattedMessage id="profile.header"/>
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <Form onSubmit={onFormSubmit} method="post">
          {errorMessage && <Alert type="error">{errorMessage}</Alert>}
          <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
            <Column columnWidth={COLUMN_WIDTH}>
              <LayoutSet>
                <Card>
                  <h3>
                    <FormattedMessage id="profile.edit.personalHeader"/>
                  </h3>

                  <InputWrapper text={errorsFields.firstName} isRequired={true}>
                    <InputField
                      inputProps={{
                        id: "firstName",
                        ...text("firstName"),
                      }}
                      a11yId="firstName"
                      // fyi: <Label> doesn't have isRequired property, doesn't show
                      // "*" to indicate that the field is required
                      label={
                        <FormattedMessage id="profile.firstName">
                          {msg => <b>{msg}</b>}
                        </FormattedMessage>
                      }
                      isRequired={true}
                    />
                  </InputWrapper>

                  <InputWrapper text={errorsFields.lastName} isRequired={true}>
                    <InputField
                      inputProps={{
                        id: "lastName",
                        ...text("lastName"),
                      }}
                      a11yId="lastName"
                      label={
                        <FormattedMessage id="profile.lastName">
                          {msg => <b>{msg}</b>}
                        </FormattedMessage>
                      }
                    />
                  </InputWrapper>

                  <InputWrapper text={errorsFields.gender} isRequired={true}>
                    <RadioGroupField
                      {...radio("gender")}
                      isHorizontal={true}
                      a11yId="gender"
                      label={
                        <FormattedMessage id="profile.gender">
                          {msg => <b>{msg}</b>}
                        </FormattedMessage>
                      }
                      options={[
                        { label: "Male", value: "male" },
                        { label: "Female", value: "female" },
                      ]}
                    />
                  </InputWrapper>

                  <InputWrapper text={errorsFields.dateBirth} isRequired={true}>
                    <InputField
                      {...raw("dateBirth")}
                      type="date"
                      a11yId="dateBirth"
                      label={
                        <FormattedMessage id="profile.dateBirth">
                          {msg => <b>{msg}</b>}
                        </FormattedMessage>
                      }
                    />
                  </InputWrapper>

                  <InputWrapper text={errorsFields.country} isRequired={true}>
                    <SelectField
                      {...select("country")}
                      a11yId="country"
                      label={
                        <FormattedMessage id="profile.country">
                          {msg => <b>{msg}</b>}
                        </FormattedMessage>
                      }
                      options={COUNTRIES_OPTIONS}
                      isRequired={true}
                    />
                  </InputWrapper>
                </Card>
              </LayoutSet>
            </Column>
          </Row>
          <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
            <Column columnWidth={COLUMN_WIDTH}>
              <LayoutSet>
                <Card>
                  <h3>
                    <FormattedMessage id="profile.edit.privacyHeader"/>
                  </h3>

                  <InputWrapper text={errorsFields.openToRecruiting}>
                    <CheckboxField
                      checkboxProps={{
                        id: "openToRecruiting",
                        ...checkbox("openToRecruiting"),
                      }}
                      type="checkbox"
                      label={<FormattedMessage id="profile.openToRecruiting"/>}
                    />
                  </InputWrapper>

                  <InputWrapper text={errorsFields.openToNewsletter}>
                    <CheckboxField
                      checkboxProps={{
                        id: "openToNewsletter",
                        ...checkbox("openToNewsletter"),
                      }}
                      type="checkbox"
                      label={<FormattedMessage id="profile.openToNewsletter"/>}
                    />
                  </InputWrapper>
                </Card>
              </LayoutSet>
            </Column>
          </Row>
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
