import React from "react";
import { Heading } from "../heading";
import { Text } from "../text";
import { Section } from "./section";

export const Standard = () => {
  return (
    <Section>
      <Heading size={1}>Section!</Heading>
      <Text size={1}>Body Body Body Body Body Body Body Body</Text>
    </Section>
  );
};

export default {
  title: "Section",
  component: Standard,
  argTypes: {},
};
