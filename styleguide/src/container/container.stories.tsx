import React from "react";
import { Container } from "./container";

export default {
  title: "Container",
};

export const Primary = () => {
  return (
    <div>
      <Container size="base">Base Container</Container>
      <Container size="small">Small Container</Container>
      <Container center={false} size="small">
        Small Container - No center align
      </Container>
      <Container center={false} size="small" noPadding>
        Small Container / No center align / No padding
      </Container>
      <Container size="medium">Medium Container</Container>
    </div>
  );
};
