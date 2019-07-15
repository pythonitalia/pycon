import React, { useState } from "react";

import { Column, Columns, Link } from "fannypack";
import styled, { css } from "styled-components";
import { theme } from "../../config/theme";
import { Button } from "../button";
import { ExpandedMenu } from "./expanded-menu";
import { Hamburger } from "./hamburger";

const LinkContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;

  a {
    margin-right: 2rem;
    text-decoration: none;
    &:last-child {
      margin-right: 0;
    }
  }
`;

const LogoContainer = styled.div<{ open: boolean }>`
  justify-content: center;
  display: flex;
  height: 100%;
  align-items: center;
  font-family: Rubik;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
  ${props =>
    props.open &&
    css`
      color: ${theme.palette.white};
    `}
`;

const MenuContainer = styled.div<{ open: boolean }>`
  display: flex;
  align-items: center;
  height: 100%;

  a {
    text-decoration: none;
    display: flex;
    align-items: center;
    outline: none;
    transition: 0.25s ease-in-out;
    &:hover {
      ${props =>
        props.open &&
        css`
          color: ${theme.palette.white};
        `}
      span {
        background: currentColor;
        ${props =>
          props.open &&
          css`
            background: ${theme.palette.white};
          `}
      }
    }
  }
`;

const Wrapper = styled.div<{ open: boolean }>`
  height: 80px;
  padding: 0 16px;
  ${props =>
    props.open &&
    css`
      background-color: ${theme.palette.primary};
      a {
        color: ${theme.palette.white};
      }
    `}
  > div,
  > div > div {
    height: 100%;
    margin-top: 0;
    margin-bottom: 0;
  }
`;

export const Topbar = () => {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <Wrapper open={showMenu}>
      <Columns>
        <Column spread={4}>
          <MenuContainer open={showMenu}>
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
          <LogoContainer open={showMenu}>PyCon Italia</LogoContainer>
        </Column>
        <Column spread={4}>
          <LinkContainer>
            <Link href="#">Login</Link>
            <Link href="#">Schedule</Link>
            <Button palette={showMenu ? "white" : "primary"}>
              GET YOUR TICKET
            </Button>
          </LinkContainer>
        </Column>
      </Columns>
      {showMenu && <ExpandedMenu />}
    </Wrapper>
  );
};
