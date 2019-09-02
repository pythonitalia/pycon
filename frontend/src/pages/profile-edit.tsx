import React, { useState } from "react";

import {
  Button,
  Card,
  Heading,
  InputField,
  LayoutSet,
  RadioGroupField,
  SelectField,
} from "fannypack";
import { Column, Container, Row } from "grigliata";
import styled from "styled-components";
import { STANDARD_ROW_PADDING } from "../config/spacing";
import { HomeLayout } from "../layouts/home";

type UserProps = {
  data: any;
};

type UserType = {
  firstName: string;
  lastName: string;
};

const Wrapper = styled.div`
  .content {
    position: relative;
    z-index: 1;
  }
`;

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

const COUNTRY_OPTIONS = [
  { label: "Select", value: "" },
  { label: "Italy", value: "IT" },
  { label: "United Kingdom", value: "GB" },
  { label: "France", value: "FR" },
  { label: "Germany", value: "DE" },
  { label: "United States of America", value: "US" },
];

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

const EditPage: React.FC = me => {
  console.log(me);
  const [errors, setErrors] = useState({});
  const [user, setUser] = useState({ ...me });
  console.log(user);
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
    <Wrapper>
      <Heading use="h3">Edit Profile</Heading>
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
              options={COUNTRY_OPTIONS}
              isRequired={true}
              validationText={errors.country}
            />
          </InputWrapper>
        </Card>

      </LayoutSet>
      <Row paddingBottom={ROW_PADDING} paddingTop={BUTTON_PADDING}>
        <Button onClick={handleUserSubmit}>Send!</Button>
      </Row>
    </Wrapper>
  );
};

export default ({ data }: UserProps) => (
  <HomeLayout>
    <Container fullWidth={false}>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <EditPage
            {...{
              firstName: "John Winston",
              lastName: "Lennon",
              gender: "male",
              dateBirth: "1940-10-09",
            }}
          />
        </Column>
      </Row>
    </Container>
  </HomeLayout>
);
