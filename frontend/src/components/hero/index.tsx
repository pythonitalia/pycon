import { theme } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import { Column, Row } from "grigliata";
import React from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";

type HeroProps = {
  backgroundImage: GatsbyImageProps | null;
  title: string;
};

const Wrapper = styled.div`
  position: relative;
  padding: 2.5rem 0 0 0;
  color: ${theme("palette.white")};

  &::before {
    content: "";
    display: block;
    background: ${theme("palette.primary")};
    top: 0;
    bottom: 0;
    left: 1rem;
    right: 1rem;
    position: absolute;
    z-index: 0;
  }

  .content {
    position: relative;
    z-index: 1;
  }

  img {
    width: 100%;
    height: auto;
  }

  header {
    position: relative;
  }

  h1 {
    position: absolute;
    bottom: 0;
    left: 16px;
    margin: 0;
    color: white;
    font-size: 35px;
    line-height: 25px;
    @media (min-width: 768px) {
      font-size: 55px;
      line-height: 45px;
    }
    @media (min-width: 1024px) {
      font-size: 92px;
      line-height: 70px;
    }
    @media (min-width: 1366px) {
      font-size: 120px;
      line-height: 92px;
    }
  }

  p {
    margin-top: 0;
  }
`;

export const Hero: React.SFC<HeroProps> = props => (
  <Wrapper>
    <div className="content">
      <header>
        <div style={{ position: "relative" }}>
          {props.backgroundImage && <Img {...props.backgroundImage} />}
          <h1>{props.title}</h1>
        </div>
      </header>

      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          paddingTop={{
            mobile: 3,
            tabletPortrait: 3,
            tabletLandscape: 3,
            desktop: 3,
          }}
          paddingBottom={{
            mobile: 3,
            tabletPortrait: 3,
            tabletLandscape: 3,
            desktop: 3,
          }}
          paddingLeft={{
            mobile: 3,
            tabletPortrait: 3,
            tabletLandscape: 3,
            desktop: 3,
          }}
          paddingRight={{
            mobile: 3,
            tabletPortrait: 3,
            tabletLandscape: 3,
            desktop: 3,
          }}
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
    </div>
  </Wrapper>
);
