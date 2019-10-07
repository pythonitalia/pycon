import { Heading } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import { Column, Container, Row } from "grigliata";
import { ColumnWidthValuesType } from "grigliata/dist/typings/column";
import React from "react";
import styled, { keyframes } from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { MaxWidthWrapper } from "../max-width-wrapper";
import { SectionTitle } from "../section-title";

const SponsorLink = styled.a`
  display: block;
  border: 1px solid #ccc;
  transition: 0.3s ease-in-out;
  filter: saturate(0);

  :hover {
    border-color: ${props => props.theme.palette.primary};
    filter: none;
  }
`;

const loveAnimation = keyframes`
  from {
    opacity: 0;
    transform: translate(-50%, -50%);
  }

  50% {
    opacity: 1;
  }
`;

const BecomeASponsorLink = styled.a`
  display: block;
  width: 100%;
  position: relative;
  color: ${props => props.theme.palette.primary};

  ::before {
    content: "";
    display: inline-block;
    padding-top: 48.5%;
  }

  > span,
  .love {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    border: 1px solid ${props => props.theme.palette.primary};
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .love {
    display: flex;
    justify-content: space-around;
  }

  .love span {
    --x: 0;
    --y: 0;
    --multiplier: 50px;
    position: absolute;
    left: 50%;
    top: 50%;
    display: inline-block;
    opacity: 0;
    transform: translate(
      calc(-50% + var(--multiplier) * (var(--x))),
      calc(-50% - var(--multiplier) * (var(--y)))
    );
  }

  .love:hover span {
    animation: ${loveAnimation} 0.4s linear;
  }
`;

type Sponsor = {
  name: string;
  link: string | null;
  imageFile: {
    childImageSharp: GatsbyImageProps | null;
  } | null;
};

type SponsorsByLevel = {
  level: string;
  sponsors: Sponsor[];
};

type SponsorListProps = {
  sponsors: SponsorsByLevel[];
};

const MARGIN_NEGATIVE_COLUMN = {
    mobile: -0.5,
    tabletPortrait: -0.5,
    tabletLandscape: -0.5,
    desktop: -0.5,
  },
  FULL_WIDTH_COLUMN: ColumnWidthValuesType = {
    mobile: 12,
    tabletPortrait: 12,
    tabletLandscape: 12,
    desktop: 12,
  };

const getSponsorLinkProps = (sponsor: Sponsor) => {
  const props: React.AnchorHTMLAttributes<HTMLAnchorElement> = {};

  if (sponsor.link) {
    props.href = sponsor.link;
    props.target = "_blank";
  }

  return props;
};

export const SponsorList: React.SFC<SponsorListProps> = props => (
  <>
    <Row paddingLeft={STANDARD_ROW_PADDING} paddingRight={STANDARD_ROW_PADDING}>
      <Column>
        <SectionTitle>Sponsors</SectionTitle>
      </Column>
    </Row>

    <Container>
      {props.sponsors.map((level, i) => (
        <Row
          key={level.level}
          marginTop={
            i === 0
              ? {
                  mobile: 1,
                  tabletPortrait: -1,
                  tabletLandscape: -3,
                  desktop: -4,
                }
              : {
                  mobile: 1,
                  tabletPortrait: 1,
                  tabletLandscape: 2,
                  desktop: 2,
                }
          }
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
        >
          <Column columnWidth={FULL_WIDTH_COLUMN}>
            <Heading use="h5">{level.level}</Heading>
          </Column>
          <Column columnWidth={FULL_WIDTH_COLUMN}>
            <Row
              marginLeft={MARGIN_NEGATIVE_COLUMN}
              marginRight={MARGIN_NEGATIVE_COLUMN}
            >
              {level.sponsors &&
                level.sponsors.map(sponsor => (
                  <Column
                    key={sponsor.name}
                    columnWidth={{
                      mobile: 12,
                      tabletPortrait: 4,
                      tabletLandscape: 3,
                      desktop: 3,
                    }}
                  >
                    <SponsorLink
                      {...getSponsorLinkProps(sponsor)}
                      title={sponsor.name}
                    >
                      {sponsor.imageFile && (
                        <Img
                          {...sponsor.imageFile.childImageSharp}
                          alt={sponsor.name}
                        />
                      )}
                    </SponsorLink>
                  </Column>
                ))}

              <Column
                columnWidth={{
                  mobile: 12,
                  tabletPortrait: 4,
                  tabletLandscape: 3,
                  desktop: 3,
                }}
              >
                <BecomeASponsorLink href="#">
                  <span>Become a sponsor</span>

                  <div className="love">
                    {Array(20)
                      .fill("💙")
                      .map((value, index) => (
                        <span
                          key={index}
                          style={{
                            ["--x" as any]:
                              Math.cos(index) + (Math.random() - 0.5),
                            ["--y" as any]:
                              Math.sin(index) + (Math.random() - 0.5),
                          }}
                        >
                          {value}
                        </span>
                      ))}
                  </div>
                </BecomeASponsorLink>
              </Column>
            </Row>
          </Column>
        </Row>
      ))}
    </Container>
  </>
);
