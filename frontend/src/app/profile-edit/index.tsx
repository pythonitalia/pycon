import { useMutation, useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import * as React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { MyProfileQuery, UpdateMutation, UpdateMutationVariables } from "../../generated/graphql-backend";
import MY_PROFILE_QUERY from "./profile-edit.graphql";
import UPDATE_MUTATION from "./update.graphql";
import {
  Button,
  Card,
  CheckboxField,
  FieldWrapper,
  InputField,
  LayoutSet,
  RadioGroupField,
  SelectField,
} from "fannypack";
import { Column, Row } from "grigliata";
import { useEffect } from "react";
import { useCallback } from "react";
import { Form } from "../../components/form";

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

export const EditProfileApp: React.SFC<RouteComponentProps> = () => {
  // define form object
  const [formState, { text, radio, select, checkbox, date }] = useFormState(
    {},
    {
      withIds: true,
    });

  // region GET_USER_DATA_FROM_BACKEND
  const setProfile = (data: MyProfileQuery) => {
    const { me } = data;
    console.log({me});

    // I know, is ugly... formState doesn't have a way to set
    // all values together
    formState.setField("firstName", me.firstName);
    formState.setField("lastName", me.lastName);
    formState.setField("gender", me.gender);
    formState.setField("dateBirth", me.dateBirth);
    formState.setField("country", me.country);
    formState.setField("openToRecruiting", me.openToRecruiting);
    formState.setField("openToNewsletter", me.openToNewsletter);
  };
  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY, { onCompleted: setProfile },
  );
  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }
  // endregion

  // region UPDATE_SEND_MUTATION
  const onUpdateComplete = (updateData: UpdateMutation) => {
    console.log({updateData});
    if (!updateData || updateData.update.__typename !== "MeUser") {
      return;
    }
    // navigate(profileUrl);
  };

  const [update, { updateLoading, updateError, updateData }] = useMutation<UpdateMutation,
    UpdateMutationVariables>(UPDATE_MUTATION, {
    onCompleted: onUpdateComplete,
  });

  if (updateError) {
    throw new Error(`Unable to save profile, ${updateError}`);
  }

  console.log({ updateLoading, updateError, updateData });

  const onFormSubmit = useCallback(
    e => {
      e.preventDefault();
      console.log("onFormSubmit! formState.values: " + JSON.stringify(formState.values));
      update({
        variables: formState.values,
      });
    },
    [update, formState],
  );
  // endregion

  const hangleUserChange = ({ target }) => {
    console.log(`hangleUserChange! ${target.id}:  ${target.value} `);
    formState.setField(target.id, target.value);
  };
  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    // Update the document title using the browser API
    console.log("Effect: formState.values: " + JSON.stringify(formState.values));
  });

  return (
    <>
      <h1>
        <FormattedMessage id="profile.header"/>
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <Form onSubmit={onFormSubmit} method="post">
          <LayoutSet>
            <Card>
              <h3>
                <FormattedMessage id="profile.edit.personalHeader"/>
              </h3>
              <InputWrapper>

                <InputField
                  inputProps={{
                    id: "firstName",
                    ...text("firstName"),
                  }}
                  a11yId="firstName"
                  // fyi: <Label> doesn't have isRequired property, doesn't show
                  // "*" to indicate that the field is required
                  label={(
                    <FormattedMessage id="profile.firstName">
                      {msg => <b>{msg}</b>}
                    </FormattedMessage>
                  )}
                  onChange={hangleUserChange}
                  isRequired={true}
                />
              </InputWrapper>

              <InputWrapper>
                <InputField
                  inputProps={{
                    id: "lastName",
                    ...text("lastName"),
                  }}
                  a11yId="lastName"
                  label={(
                    <FormattedMessage id="profile.lastName">
                      {msg => <b>{msg}</b>}
                    </FormattedMessage>
                  )}
                  onChange={hangleUserChange}
                  isRequired={true}
                />
              </InputWrapper>

              <InputWrapper>
                <RadioGroupField
                  {...radio("gender")}
                  value={formState.gender}
                  isHorizontal={true}
                  a11yId="gender"
                  label={(
                    <FormattedMessage id="profile.gender">
                      {msg => <b>{msg}</b>}
                    </FormattedMessage>
                  )}
                  onChange={hangleUserChange}
                  options={[
                    { label: "Male", value: "male" },
                    { label: "Female", value: "female" },
                  ]}
                />
              </InputWrapper>

              <InputWrapper>
                <InputField
                  {...date("dateBirth")}
                  value={formState.dateBirth}
                  type="date"
                  data-date-format="YYYY-MM-DD"
                  a11yId="dateBirth"
                  label={(
                    <FormattedMessage id="profile.dateBirth">
                      {msg => <b>{msg}</b>}
                    </FormattedMessage>
                  )}
                  onChange={hangleUserChange}
                />
              </InputWrapper>

              <InputWrapper>
                <SelectField
                  {...select("country")}
                  a11yId="country"
                  label={(
                    <FormattedMessage id="profile.country">
                      {msg => <b>{msg}</b>}
                    </FormattedMessage>
                  )}
                  onChange={hangleUserChange}
                  options={[
                    { label: "Select", value: "" },
                    { label: "Italy", value: "IT" },
                  ]}
                  isRequired={true}
                />
              </InputWrapper>
            </Card>
          </LayoutSet>

          <LayoutSet>
            <Card>
              <h3>
                <FormattedMessage id="profile.edit.privacyHeader"/>
              </h3>

              <FieldWrapper
                //validationText={}
                //state={ ? "danger" : ""}
              >
                <CheckboxField
                  checkboxProps={{
                    id: "openToRecruiting",
                    ...checkbox("openToRecruiting"),
                    isRequired: true,
                  }}
                  type="checkbox"
                  label={(<FormattedMessage id="profile.openToRecruiting"/>)}
                />
              </FieldWrapper>


              <FieldWrapper
                //validationText={}
                //state={ ? "danger" : ""}
              >
                <CheckboxField
                  checkboxProps={{
                    id: "openToNewsletter",
                    ...checkbox("openToNewsletter"),
                    isRequired: true,
                  }}
                  type="checkbox"
                  label={(<FormattedMessage id="profile.openToNewsletter"/>)}
                />
              </FieldWrapper>

            </Card>
          </LayoutSet>

          <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
            <Button
              size="medium"
              palette="primary"
              isLoading={loading}
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
