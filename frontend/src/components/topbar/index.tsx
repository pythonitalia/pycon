import { Column, Columns, Link } from "fannypack";
import React, { useState } from "react";
import styled from "styled-components";
import { theme } from "../../config/theme";
import { Button } from "../button";
import { Hamburger } from "./hamburger";

const LinkContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: right;
  height: 100%;

  a {
    margin-right: 2rem;
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

const MenuContainer = styled.div`
  display: flex;
  align-items: center;
  height: 100%;

  a {
    text-decoration: none;
    display: flex;
    align-items: center;
    outline: none;
    transition: 0.25s ease-in-out;
    &:hover span {
      background: #435a6f;
    }
  }
`;

const Wrapper = styled.div`
  height: 80px;
  padding: 0 16px;

  > div,
  > div > div {
    height: 100%;
  }
`;

export const Topbar = () => {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <Wrapper>
      <Columns>
        <Column spread={4}>
          <MenuContainer>
            <Link
              href="#"
              onClick={e => {
                e.preventDefault();
                setShowMenu(!showMenu);
              }}
            >
              <Hamburger open={showMenu} /> Menu
            </Link>
          </MenuContainer>
        </Column>
        <Column spread={4}>
          <LogoContainer>PyCon Italia</LogoContainer>
        </Column>
        <Column spread={4}>
          <LinkContainer>
            <Link href="#">Login</Link>
            <Link href="#">Schedule</Link>
            <Button palette="primary">GET YOUR TICKET</Button>
          </LinkContainer>
        </Column>
      </Columns>
    </Wrapper>
  );
};
