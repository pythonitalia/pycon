import styled from "styled-components";
import { theme } from "../../config/theme";

export const Wrapper = styled.div`
  margin-top: 3rem;
  background-color: ${theme.palette.primary};
  color: ${theme.palette.white};
  position: relative;
  display: block;
  padding-bottom: 0.5rem;
  h3 {
    margin-top: 0;
  }
  .margin-mobile-0-r {
    margin-bottom: 4rem;
  }
  @media only screen and (min-width: 578px) {
    .margin-mobile-0-r,
    .margin-mobile-0-l {
      margin: 0;
      margin-bottom: 4rem;
    }
  }
  @media only screen and (min-width: 992px) {
    .margin-mobile-0-r {
      margin-right: 4rem;
      margin-bottom: 0;
    }
    .margin-mobile-0-l {
      margin-left: 4rem;
      margin-bottom: 0;
    }
  }
`;
