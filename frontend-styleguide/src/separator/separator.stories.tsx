import React from "react";
import { Container } from "../container";
import { Separator } from "./separator";

export default {
  title: "Separator",
};

export const Primary = () => {
  return (
    <Container>
      Test
      <Separator />
      Another separator
    </Container>
  );
};

export const EscapeContainer = () => {
  return (
    <>
      <Container>
        Mobile only
        <Separator escapeContainer="mobile" />
        Another separator
      </Container>
      <Container>
        Always
        <Separator escapeContainer={true} />
        Another separator
      </Container>
    </>
  );
};
