import { graphql, Link, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React, { useContext } from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { theme } from "../../config/theme";
import { LanguageContext } from "../../context/language";
import { ExpandedMenuQuery } from "../../generated/graphql";
import { MaxWidthWrapper } from "../max-width-wrapper";

const Headings = styled.div`
  border-top: 1px solid ${theme.palette.white};
  padding-top: 0px;
  margin: 0.5rem 0;

  @media (min-width: 992px) {
    margin: 5rem auto;
  }
  p {
    margin-bottom: 0;
    margin-top: 0.5rem;

    @media (min-width: 992px) {
      margin-top: 1rem;
    }
  }
`;

const Base = ({ ...props }) => {
  // we can't pass variables to static queries so we have to
  // fetch both languages
  const {
    backend: {
      conference: {
        programMenuEn,
        conferenceMenuEn,
        programMenuIt,
        conferenceMenuIt,
      },
    },
  } = useStaticQuery<ExpandedMenuQuery>(graphql`
    query ExpandedMenu {
      backend {
        conference {
          programMenuEn: menu(identifier: "program-nav") {
            title(language: "en")
            links {
              title(language: "en")
              href(language: "en")
              isPrimary
            }
          }
          conferenceMenuEn: menu(identifier: "conference-nav") {
            title(language: "en")
            links {
              title(language: "en")
              href(language: "en")
              isPrimary
            }
          }
          programMenuIt: menu(identifier: "program-nav") {
            title(language: "it")
            links {
              title(language: "it")
              href(language: "it")
              isPrimary
            }
          }
          conferenceMenuIt: menu(identifier: "conference-nav") {
            title(language: "it")
            links {
              title(language: "it")
              href(language: "it")
              isPrimary
            }
          }
        }
      }
    }
  `);

  const language = useContext(LanguageContext);

  const menusEn = [programMenuEn, conferenceMenuEn].filter(menu => !!menu);
  const menusIt = [programMenuIt, conferenceMenuIt].filter(menu => !!menu);

  const menus = language === "it" ? menusIt : menusEn;

  return (
    <div {...props}>
      <MaxWidthWrapper className="expanded_menu">
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
          {menus.map((menu, i) => (
            <Column
              key={i}
              columnWidth={{
                mobile: 12,
                tabletPortrait: 6,
                tabletLandscape: 4,
                desktop: 4,
              }}
            >
              <Headings>
                <h3>{menu!.title}</h3>

                {menu!.links.map((link, index) => (
                  <p key={index}>
                    <Link to={link.href}>{link.title}</Link>
                  </p>
                ))}
              </Headings>
            </Column>
          ))}
        </Row>
      </MaxWidthWrapper>
    </div>
  );
};

export const ExpandedMenu = styled(Base)`
  position: fixed;
  width: 100%;
  top: 80px;
  left: 0;
  background-color: ${theme.palette.primary};

  a {
    text-decoration: none;
    color: ${theme.palette.white};
  }

  a:hover {
    text-decoration: underline;
  }

  .expanded_menu {
    overflow-y: scroll;
    height: calc(100% - 80px);
  }
`;
