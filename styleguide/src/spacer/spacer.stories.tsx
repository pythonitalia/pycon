import React from "react";
import { Paragraph } from "../paragraph/paragraph";
import { Spacer } from "./spacer";

export default {
  title: "Spacer",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => (
  <>
    <Paragraph>Block of text Block of text Block of text</Paragraph>
    <Spacer size="medium" />
    <Paragraph>Block of text Block of text Block of text</Paragraph>
  </>
);
