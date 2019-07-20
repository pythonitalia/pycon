import { Text } from "fannypack";
import styled from "styled-components";

export const SectionTitle = styled(Text).attrs({
  use: "h1",
})`
  font-family: Rubik;
  font-style: normal;
  font-weight: bold;
  font-size: 56px;
  line-height: 56px;
  text-transform: uppercase;
  margin-top: 2rem;
  color: ${props => props.theme.palette.primaryTint};
  @media (min-width: 768px) {
    font-size: 56px;
    line-height: 56px;
  }
  @media (min-width: 992px) {
    font-size: 120px;
    line-height: 120px;
  }
  @media (min-width: 1200px) {
    font-size: 200px;
    line-height: 200px;
  }
`;
