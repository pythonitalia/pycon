import React, { useState } from "react";

import { Card, Heading, InputField, LayoutSet } from "fannypack";
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
        </Card>
      </LayoutSet>
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
          <EditPage {...{ firstName: "Ester", lastName: "Beltrami" }} />
        </Column>
      </Row>
    </Container>
  </HomeLayout>
);
