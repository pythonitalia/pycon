import React from "react";

import styled from "styled-components";
import { theme } from "../../config/theme";
import { CustomColumn } from "../column";
import { CustomColumns } from "../columns";

const Wrapper = styled.div`
  div[class^="columns__CustomColumns"] {
    display: block;

    @media (min-width: 992px) {
      display: flex;
    }
  }
`;

const Headings = styled.div`
  border-top: 1px solid ${theme.palette.white};
  padding-top: 0px;
  margin: 0.5rem 0;

  @media (min-width: 992px) {
    margin: 5rem auto;
  }
  p {
    margin-bottom: 0;
    margin-top: 0.5rem;

    @media (min-width: 992px) {
      margin-top: 1rem;
    }
  }
`;

const Base = ({ ...props }) => {
  return (
    <div {...props}>
      <Wrapper>
        <CustomColumns>
          <CustomColumn>
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
          </CustomColumn>
          <CustomColumn>
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
          </CustomColumn>
          <CustomColumn>
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
          </CustomColumn>
        </CustomColumns>
      </Wrapper>
    </div>
  );
};

export const ExpandedMenu = styled(Base)`
  position: fixed;
  width: 100%;
  top: 80px;
  left: 0;
  background-color: ${theme.palette.primary};
  color: ${theme.palette.white};
  padding: 16px;
  overflow: scroll;
  .expanded_menu {
    div {
      height: calc(100% - 80px);
    }
  }
`;
