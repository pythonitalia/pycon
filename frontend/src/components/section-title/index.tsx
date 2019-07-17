import { Text } from "fannypack";
import styled from "styled-components";

export const SectionTitle = styled(Text).attrs({
  use: "h1",
})`
  font-family: Rubik;
  font-style: normal;
  font-weight: bold;
  font-size: 200px;
  line-height: 200px;
  text-transform: uppercase;
  margin-top: 0.5em;

  color: ${props => props.theme.palette.primaryTint};
`;
