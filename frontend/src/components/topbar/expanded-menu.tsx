import React from "react";
import styled from "styled-components";
import { theme } from "../../config/theme";
import { Columns, Column } from "fannypack";

const Headings = styled.div`
  border-top: 1px solid ${theme.palette.white};
  margin: 5rem auto;
  width: 90%;
  padding-top: 0px;
`;

const Base = ({ ...props }) => {
  return (
    <div {...props}>
      <Columns>
        <Column spread={6}>
          <Headings>
            <h3>Heading</h3>
            <p>
              <a href="#">Linkoone</a>
            </p>
            <p>
              <a href="#">Link</a>
            </p>
            <p>
              <a href="#">Linkoone</a>
            </p>
          </Headings>
        </Column>
        <Column>
          <Headings>
            <h3>Heading</h3>
            <p>
              <a href="#">Associazione</a>
            </p>
            <p>
              <a href="#">Linkoone</a>
            </p>
            <p>
              <a href="#">Linkoone</a>
            </p>
            <p>
              <a href="#">Linkettonino</a>
            </p>
            <p>
              <a href="#">Link hello</a>
            </p>
          </Headings>
        </Column>
        <Column>
          <Headings>
            <h3>Heading</h3>
            <p>
              <a href="#">Linkoone</a>
            </p>
            <p>
              <a href="#">Link for try</a>
            </p>
            <p>
              <a href="#">Link</a>
            </p>
            <p>
              <a href="#">Linkoone</a>
            </p>
          </Headings>
        </Column>
      </Columns>
    </div>
  );
};

export const ExpandedMenu = styled(Base)`
  position: fixed;
  width: 100%;
  height: calc(100% - 80px);
  top: 80px;
  left: 0;
  background-color: ${theme.palette.primary};
  color: ${theme.palette.white};
  padding: 16px;
`;
