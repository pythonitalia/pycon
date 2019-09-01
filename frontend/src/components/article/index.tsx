import { GatsbyImageProps } from "gatsby-image";
import { Row } from "grigliata";
import React from "react";
import styled from "styled-components";

import { Hero } from "../hero";
import { ArticleTitle } from "./title";

const Wrapper = styled.div`
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

  ${ArticleTitle} {
    margin-bottom: 0.3em;

    @media (min-width: 1024px) {
      font-size: 42px;
      line-height: 32px;
    }
    @media (min-width: 1366px) {
      font-size: 90px;
      line-height: 72px;
    }
  }

  p {
    margin-top: 0;
  }
`;

type ArticleProps = {
  hero: GatsbyImageProps | null;
  title: string;
  description?: string;
};

export const Article: React.SFC<ArticleProps> = props => (
  <Wrapper>
    <Hero title={props.title} backgroundImage={props.hero}>
      {props.description && <p> {props.description} </p>}
    </Hero>
    <Row
      marginTop={{
        mobile: 2,
        tabletPortrait: 2,
        tabletLandscape: 2,
        desktop: 2,
      }}
      paddingLeft={{
        mobile: 2,
        tabletPortrait: 2,
        tabletLandscape: 2,
        desktop: 2,
      }}
      paddingRight={{
        mobile: 2,
        tabletPortrait: 2,
        tabletLandscape: 2,
        desktop: 2,
      }}
    >
      <div className="content">{props.children}</div>
    </Row>
  </Wrapper>
);
