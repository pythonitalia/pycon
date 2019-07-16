import React from "react";

import { theme } from "fannypack";
import styled from "styled-components";
import { Button } from "../button";

type HeroProps = {
  // TODO: use gatsby images
  backgroundImage: string;
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
    padding: 0 20px;
  }

  article {
    padding: 0 40px;
  }

  footer {
    text-align: right;
  }
`;

export const Hero = (props: HeroProps) => (
  <Wrapper>
    <div className="content">
      <header>
        <img src={props.backgroundImage} />
        <h1>Title!!1</h1>
      </header>

      <article>
        <h2>Subssssssssssssssss</h2>

        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Deserunt
          recusandae cumque suscipit, quam ullam sit id placeat sequi modi ipsum
          inventore. Tempore dolorem vero fugiat eum adipisci cupiditate eos
          ullam!
        </p>

        <footer>
          <Button>LOL</Button>
        </footer>
      </article>
    </div>
  </Wrapper>
);
