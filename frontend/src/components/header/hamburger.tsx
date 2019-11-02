import React from "react";
import styled, { css } from "styled-components";

import { theme } from "../../config/theme";
import { ExpandableProps } from "./types";

const Draw = styled.div<ExpandableProps>`
  width: 40px;
  height: 24px;
  margin-right: 0.5rem;
  position: relative;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out transform;
  cursor: pointer;

  span {
    display: block;
    position: absolute;
    height: 4px;
    width: 100%;
    background: ${theme.palette.primary};
    border-radius: 9px;
    opacity: 1;
    transform: rotate(0deg);
    transition: 0.25s ease-in-out transform;
  }

  span:nth-child(1) {
    top: 0px;
  }

  span:nth-child(2) {
    top: 10px;
  }

  span:nth-child(3) {
    top: 20px;
  }

  ${props =>
    props.open &&
    css`
      span:nth-child(1) {
        top: 10px;
        transform: rotate(135deg);
      }
      span:nth-child(2) {
        opacity: 0;
        left: -60px;
      }
      span:nth-child(3) {
        top: 10px;
        transform: rotate(-135deg);
      }
      span {
        background: ${theme.palette.white};
        left: -4px;
      }
    `}
`;

export const Hamburger = ({ open }: ExpandableProps) => (
  <div>
    <Draw open={open}>
      <span />
      <span />
      <span />
    </Draw>
  </div>
);
