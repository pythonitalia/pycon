import React from "react";
import { Separator } from "./separator";
import { Container } from "../container";

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
