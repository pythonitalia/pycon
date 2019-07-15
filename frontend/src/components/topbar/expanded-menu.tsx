import React from "react";
import styled from "styled-components";
import { theme } from "../../config/theme";

const Base = ({ ...props }) => {
  return <div {...props}>asdfasdf</div>;
};

export const ExpandedMenu = styled(Base)`
  position: fixed;
  width: 100%;
  height: calc(100% - 80px);
  top: 80px;
  left: 0;
  background-color: ${theme.palette.primary};
`;
