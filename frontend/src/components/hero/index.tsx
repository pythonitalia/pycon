import React from "react";

import { theme } from "fannypack";
import Img, { GatsbyImageProps } from "gatsby-image";
import styled from "styled-components";
import { CustomColumns } from "../columns";

type HeroProps = {
  backgroundImage: GatsbyImageProps;
  title: string;
};

const Wrapper = styled.div`
  position: relative;
  padding: 40px 0;
  color: ${theme("palette.white")};

  &::before {
    content: "";
    display: block;
    background: ${theme("palette.primary")};
    top: 0;
    bottom: 0;
    left: 20px;
    right: 20px;
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
    margin: 0;

    color: white;
  }

  p {
    margin-top: 0;
  }
`;

const padding = { desktop: 2, mobile: 3 };

export const Hero: React.SFC<HeroProps> = props => (
  <Wrapper>
    <div className="content">
      <header>
        <Img {...props.backgroundImage} />
        <CustomColumns as="h1" paddingLeft={padding} paddingRight={padding}>
          {props.title}
        </CustomColumns>
      </header>

      <CustomColumns
        as="article"
        paddingLeft={padding}
        paddingRight={padding}
        paddingTop={padding}
      >
        {props.children}
      </CustomColumns>
    </div>
  </Wrapper>
);
