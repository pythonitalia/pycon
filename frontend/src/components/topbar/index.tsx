import React from "react";

import { Column, Columns, Link } from "fannypack";
import styled, { css } from "styled-components";
import { theme } from "../../config/theme";
import { useToggle } from "../../helpers/use-toggle";
import { Button } from "../button";
import { ExpandedMenu } from "./expanded-menu";
import { Hamburger } from "./hamburger";
import { ExpandableProps } from "./types";

const LinkContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  display: none;
  @media (min-width: 992px) {
    display: flex;
  }
  a {
    margin-right: 2rem;
    text-decoration: none;
    &:last-child {
      margin-right: 0;
    }
  }
`;

const LogoContainer = styled.div<ExpandableProps>`
  display: flex;
  height: 100%;
  align-items: center;
  font-family: Rubik;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
  justify-content: center;
  ${props =>
    props.open &&
    css`
      color: ${theme.palette.white};
    `}
`;

const MenuContainer = styled.div<ExpandableProps>`
  display: flex;
  align-items: center;
  height: 100%;

  a {
    text-decoration: none;
    display: flex;
    align-items: center;
    outline: none;
    transition: 0.25s ease-in-out;
    .label {
      display: none;
      @media (min-width: 992px) {
        display: inline-block;
      }
    }
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

const Wrapper = styled.div<ExpandableProps>`
  height: 80px;
  padding: 0 16px;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  z-index: 10;
  background-color: ${theme.palette.white};
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
  const [isMenuOpen, toggleMenu] = useToggle(false);

  return (
    <Wrapper open={isMenuOpen}>
      <Columns>
        <Column spread={4} spreadMobile={2} spreadDesktop={4}>
          <MenuContainer open={isMenuOpen}>
            <Link
              href="#"
              onClick={e => {
                e.preventDefault();
                toggleMenu();
              }}
            >
              <Hamburger open={isMenuOpen} />{" "}
              <span className="label">Menu</span>
            </Link>
          </MenuContainer>
        </Column>
        <Column spreadMobile={8} spreadDesktop={4}>
          <LogoContainer open={isMenuOpen}>PyCon Italia</LogoContainer>
        </Column>
        <Column spread={4}>
          <LinkContainer>
            <Link href="#">Login</Link>
            <Link href="#">Schedule</Link>
            <Button palette={isMenuOpen ? "white" : "primary"}>
              GET YOUR TICKET
            </Button>
          </LinkContainer>
        </Column>
      </Columns>
      {isMenuOpen && <ExpandedMenu className="expanded_menu" />}
    </Wrapper>
  );
};
