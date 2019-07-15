import React from "react";
import styled, { css } from "styled-components";
import { theme } from "../../config/theme";

type DrawProps = {
  open: boolean;
};

const Draw = styled.div<DrawProps>`
  width: 40px;
  height: 24px;
  margin-right: 0.5rem;
  position: relative;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out;
  cursor: pointer;

  span {
    display: block;
    position: absolute;
    height: 4px;
    width: 100%;
    background: ${theme.palette.primary};
    border-radius: 9px;
    opacity: 1;
    left: 0;
    transform: rotate(0deg);
    transition: 0.25s ease-in-out;
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
      }
    `}
`;

export const Hamburger = ({ open }: { open: boolean }) => {
  console.log(open);

  return (
    <div>
      <Draw open={open}>
        <span></span>
        <span></span>
        <span></span>
      </Draw>
    </div>
  );
};
// className={open ? "open" : ""}
