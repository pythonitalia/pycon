import React from "react";

import { theme } from "fannypack";
import styled from "styled-components";
import { Button } from "../button";
import { CustomColumns } from "../columns";

type HeroProps = {
  // TODO: use gatsby images
  backgroundImage: string;
  title: string;
};

const Wrapper = styled.div`
  position: relative;
  padding: 20px 0;
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
`;

const padding = {
  left: { desktop: 2, mobile: 3 },
  right: { desktop: 2, mobile: 3 },
};

export const Hero: React.SFC<HeroProps> = props => (
  <Wrapper>
    <div className="content">
      <header>
        <img src={props.backgroundImage} />
        <CustomColumns
          as="h1"
          paddingLeft={padding.left}
          paddingRight={padding.right}
        >
          {props.title}
        </CustomColumns>
      </header>

      <CustomColumns
        as="article"
        paddingLeft={padding.left}
        paddingRight={padding.right}
      >
        <p>{props.children}</p>
      </CustomColumns>
    </div>
  </Wrapper>
);
