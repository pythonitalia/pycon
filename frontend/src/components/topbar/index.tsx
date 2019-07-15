import { Column, Columns } from "fannypack";
import React from "react";
import styled from "styled-components";
import { Button } from "../button";
import { Link } from "fannypack";

const LinkContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: right;
  height: 100%;

  a {
    margin-right: 1.5rem;
    text-decoration: none;
    &:last-child {
      margin-right: 0;
    }
  }
`;

const LogoContainer = styled.div`
  justify-content: center;
  display: flex;
  height: 100%;
  align-items: center;
  font-family: Rubik;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
`;

const Background = styled.div`
  height: 80px;
`;

const StyledColumns = styled(Columns)`
  height: 100%;
`;

const StyledColumn = styled(Column)`
  height: 100%;
`;

export const Topbar = ({ className }: any) => {
  return (
    <Background className={className}>
      <StyledColumns>
        <StyledColumn spread={4}>.</StyledColumn>
        <StyledColumn spread={4}>
          <LogoContainer>PyCon Italia</LogoContainer>
        </StyledColumn>
        <StyledColumn spread={4}>
          <LinkContainer>
            <Link href="#">Schedule</Link>
            <Link href="#">Speaker</Link>
            <Link href="#">FAQ</Link>
            <Button palette="primary">GET YOUR TICKET</Button>
          </LinkContainer>
        </StyledColumn>
      </StyledColumns>
    </Background>
  );
};
