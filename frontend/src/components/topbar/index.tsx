import { Link } from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React from "react";
import styled, { css } from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { theme } from "../../config/theme";
import { HeaderNavQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";
import { Button } from "../button";
import { MaxWidthWrapper } from "../max-width-wrapper";
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
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  height: 100%;
  align-items: center;
  font-family: Rubik;
  font-style: normal;
  font-weight: normal;
  font-size: 24px;
  justify-content: center;
  color: inherit;
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

    &:hover,
    &:focus {
      color: inherit;
    }
  }
`;

const Wrapper = styled.div<ExpandableProps>`
  height: 80px;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  z-index: 10;
  background-color: ${theme.palette.white};
  color: ${theme.palette.primary};

  ${props =>
    props.open &&
    css`
      background-color: ${theme.palette.primary};
      color: ${theme.palette.white};
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
  const {
    backend: {
      conference: { menu },
    },
  } = useStaticQuery<HeaderNavQuery>(graphql`
    query HeaderNav {
      backend {
        conference {
          menu(identifier: "header-nav") {
            links {
              title
              href
              isPrimary
            }
          }
        }
      }
    }
  `);

  const { links } = menu!;

  return (
    <Wrapper open={isMenuOpen}>
      <MaxWidthWrapper>
        <LogoContainer open={isMenuOpen}>PyCon Italia</LogoContainer>

        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
          <Column
            columnWidth={{
              mobile: 3,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
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
          <Column
            columnWidth={{
              mobile: 0,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
            <LinkContainer>
              {links.map((link, i) => {
                if (link.isPrimary) {
                  return (
                    <Button key={i} palette={isMenuOpen ? "white" : "primary"}>
                      {link.title}
                    </Button>
                  );
                }

                // TODO: don't use button for the primary link, rather use a custom
                // link that looks like the button

                return (
                  <Link key={i} href={link.href}>
                    {link.title}
                  </Link>
                );
              })}
            </LinkContainer>
          </Column>
        </Row>
      </MaxWidthWrapper>
      {isMenuOpen && <ExpandedMenu />}
    </Wrapper>
  );
};
