import { css, keyframes } from "emotion";
import React from "react";

type MarqueeProps = {
  message: string;
};

const animation = keyframes`
  0% { transform: translate(0, 0); }
  100% { transform: translate(-100%, 0); }
`;

const style = css`
  font-family: aktiv-grotesk-extended, sans-serif;
  font-size: 24px;
  line-height: 31px;
  height: 125px;
  text-transform: uppercase;
  border-top: 3px solid #000000;
  border-bottom: 3px solid #000000;
  display: flex;
  align-items: center;
  white-space: nowrap;

  span {
    will-change: transform;
    animation: ${animation} 20s linear infinite;
  }
`;

export const Marquee: React.SFC<MarqueeProps> = ({ message }) => (
  <div className={style}>
    <span>{new Array(10).fill(message).join(" / ")}</span>
  </div>
);
