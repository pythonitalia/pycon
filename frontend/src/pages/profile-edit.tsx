import React, { useState } from "react";

import {
  Button,
  Card,
  Heading,
  InputField,
  LayoutSet,
  RadioGroup,
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
              a11yId="dateBirth"
              label="Birth Date"
              value={user.dateBirth}
              onChange={hangleUserChange}
              validationText={errors.dateBirth}
            />
          </InputWrapper>
        </Card>

        <Card title="Address">
          <InputWrapper>
            <InputField
              a11yId="address"
              label="Address"
              value={user.address}
              onChange={hangleUserChange}
              validationText={errors.address}
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

        <Card title="Company Info">
          <InputWrapper>
            <InputField
              a11yId="businessName"
              label="Business Name"
              value={user.businessName}
              onChange={hangleUserChange}
              validationText={errors.businessName}
            />
          </InputWrapper>

          <InputWrapper>
            <InputField
              a11yId="fiscalCode"
              maxLength={16}
              label="Fiscal Code"
              value={user.fiscalCode}
              onChange={hangleUserChange}
              validationText={errors.fiscalCode}
            />
          </InputWrapper>

          <InputWrapper>
            <InputField
              a11yId="vatNumber"
              label="VAT Number"
              value={user.vatNumber}
              onChange={hangleUserChange}
              validationText={errors.vatNumber}
            />
          </InputWrapper>

          <InputWrapper>
            <InputField
              a11yId="phoneNumber"
              maxLength={16}
              label="Phone Number"
              value={user.phoneNumber}
              onChange={hangleUserChange}
              validationText={errors.phoneNumber}
            />
          </InputWrapper>

          <InputWrapper>
            <InputField
              a11yId="recipientCode"
              maxLength={7}
              label="Recipient Code *(Italian Company Only)"
              value={user.recipientCode}
              onChange={hangleUserChange}
              validationText={errors.recipientCode}
            />
          </InputWrapper>

          <InputWrapper>
            <InputField
              a11yId="pecAddress"
              maxLength={7}
              label="PEC Address *(Italian Company Only)"
              value={user.pecAddress}
              onChange={hangleUserChange}
              validationText={errors.pecAddress}
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
              dateBirth: "09/10/1940",
            }}
          />
        </Column>
      </Row>
    </Container>
  </HomeLayout>
);
