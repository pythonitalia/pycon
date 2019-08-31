import React from "react";

import { Heading } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import { Column, Row } from "grigliata";
import { ColumnWidthValuesType } from "grigliata/dist/typings/column";
import styled from "styled-components";
import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { SectionTitle } from "../section-title";

const SponsorLink = styled.a`
  display: block;
  border: 1px solid #ccc;
`;

const BecomeASponsorLink = styled.a`
  display: block;
  width: 100%;
  position: relative;

  ::before {
    content: "";
    display: inline-block;
    padding-top: 48.5%;
  }

  span {
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
              </BecomeASponsorLink>
            </Column>
          </Row>
        </Column>
      </Row>
    ))}
  </>
);
