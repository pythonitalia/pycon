import { theme } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import { Column, Row } from "grigliata";
import React from "react";
import styled, { css } from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";

type HeroProps = {
  backgroundImage: GatsbyImageProps | null;
  title: string;
  subtitle?: string;
};

const Wrapper = styled.div<HeroProps>`
  position: relative;
  color: ${theme("palette.primary")};

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
    font-size: 35px;
    line-height: 25px;
    margin: 2rem 0;

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

  ${props =>
    props.backgroundImage &&
    css`
      color: ${theme("palette.white")};

      h1 {
        position: absolute;
        bottom: 0;
        left: 16px;
        margin: 0;
      }
    `}
`;

const Bar = styled.div<{ subtitle?: boolean }>`
  background: ${theme("palette.primary")};
  margin: 0 1rem;
  min-height: 2rem;

  ${props =>
    props.subtitle &&
    css`
      padding: 2rem;
    `}
`;

export const Hero: React.SFC<HeroProps> = props => (
  <Wrapper {...props}>
    {props.backgroundImage && <Bar />}

    <div style={{ position: "relative" }}>
      {props.backgroundImage && <Img {...props.backgroundImage} />}
      <h1>{props.title}</h1>
    </div>

    {(props.subtitle || props.backgroundImage) && (
      <Bar subtitle={true}>{props.subtitle}</Bar>
    )}
  </Wrapper>
);
