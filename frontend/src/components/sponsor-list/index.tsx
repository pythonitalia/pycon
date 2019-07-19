import React from "react";

import { Heading } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import styled from "styled-components";
import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { Column, ColumnWidthValuesType } from "../column";
import { Row } from "../row";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div``;

type Sponsor = Array<{
  category: string;
  logos: Array<{ name: string; logo: GatsbyImageProps; link: string }>;
}>;

type SponsorListProps = {
  sponsors: Sponsor;
};

const MARGIN_NEGATIVE_COLUMN = {
  mobile: -0.5,
  tabletPortrait: -0.5,
  tabletLandscape: -0.5,
  desktop: -0.5,
};
const FULL_WIDTH_COLUMN: ColumnWidthValuesType = {
  mobile: 12,
  tabletPortrait: 12,
  tabletLandscape: 12,
  desktop: 12,
};

export const SponsorList: React.SFC<SponsorListProps> = props => {
  return (
    <Wrapper>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column>
          <SectionTitle>Sponsors</SectionTitle>
        </Column>
      </Row>
      {props.sponsors.map((o, i) => {
        return (
          <Row
            key={i}
            marginTop={
              i === 0
                ? {
                    mobile: 1,
                    tabletPortrait: -1,
                    tabletLandscape: -4,
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
            <Column colWidth={FULL_WIDTH_COLUMN}>
              <Heading use="h5">{o.category}</Heading>
            </Column>
            <Column colWidth={FULL_WIDTH_COLUMN}>
              <Row
                marginLeft={MARGIN_NEGATIVE_COLUMN}
                marginRight={MARGIN_NEGATIVE_COLUMN}
              >
                {o.logos.map((sponsor, logosKey) => {
                  return (
                    <Column
                      key={logosKey}
                      colWidth={{
                        mobile: 12,
                        tabletPortrait: 4,
                        tabletLandscape: 3,
                        desktop: 3,
                      }}
                    >
                      <a href={sponsor.link}>
                        <Img {...sponsor.logo} alt={sponsor.name} />
                      </a>
                    </Column>
                  );
                })}
              </Row>
            </Column>
          </Row>
        );
      })}
    </Wrapper>
  );
};
