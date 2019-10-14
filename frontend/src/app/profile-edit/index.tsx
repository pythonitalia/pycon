import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import * as React from "react";
import { FormattedMessage } from "react-intl";

import { MeUser, MyProfileQuery } from "../../generated/graphql-backend";
import MY_PROFILE_QUERY from "./profile-edit.graphql";
import { Button, Card, Heading, InputField, LayoutSet, RadioGroupField, SelectField } from "fannypack";
import { Column, Row } from "grigliata";
import { useState } from "react";


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
  const [errors, setErrors] = useState({});
  const [user, setUser] = useState({});

  const setProfile = (data) => {
    const { me } = data;
    console.log("onCompleted: " + JSON.stringify(me));
    setUser(() => (me));
    console.log("user: " + JSON.stringify(user));
  };
  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY, {onCompleted: setProfile}
  );

  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }

  const hangleUserChange = ({ target }) => {
    setUser(() => ({
      ...user,
      [target.id]: target.value,
    }));
  };

  const handleUserSubmit = event => {
    console.log(user);
  };

  return (
    <>
      <h1>
        <FormattedMessage id="profile.header"/>
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <>
          <LayoutSet>
            <Card title="Personal Info">
              <InputWrapper>
                <InputField
                  a11yId="firstName"
                  label="First Name"
                  value={user.firstName}
                  onChange={hangleUserChange}
                  isRequired={true}
                  validationText={errors.firstName}
                />
              </InputWrapper>

              <InputWrapper>
                <InputField
                  a11yId="lastName"
                  label="Last Name"
                  value={user.lastName}
                  onChange={hangleUserChange}
                  isRequired={true}
                  validationText={errors.lastName}
                />
              </InputWrapper>

              <InputWrapper>
                <RadioGroupField
                  isHorizontal={true}
                  label="Gender"
                  a11yId="gender"
                  name="gender"
                  value={user.gender}
                  onChange={hangleUserChange}
                  validationText={errors.gender}
                  options={[
                    { label: "Male", value: "male" },
                    { label: "Female", value: "female" },
                  ]}
                />
              </InputWrapper>

              <InputWrapper>
                <InputField
                  type="date"
                  data-date-format="DD/MM/YYYY"
                  a11yId="dateBirth"
                  label="Birth Date"
                  value={user.dateBirth}
                  onChange={hangleUserChange}
                  validationText={errors.dateBirth}
                />
              </InputWrapper>

              <InputWrapper>
                <SelectField
                  a11yId="country"
                  label="Country"
                  value={user.country}
                  onChange={hangleUserChange}
                  options={[
                    { label: "Select", value: "" },
                    { label: "Italy", value: "IT" },
                  ]}
                  isRequired={true}
                  validationText={errors.country}
                />
              </InputWrapper>
            </Card>
          </LayoutSet>
          <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
            <Button onClick={handleUserSubmit}>Send!</Button>
          </Row>
        </>
      )}
    </>
  );
};
