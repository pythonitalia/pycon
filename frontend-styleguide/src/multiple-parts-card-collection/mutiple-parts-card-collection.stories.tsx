import React from "react";
import { Heading } from "../heading";
import { CardPart } from "../multiple-parts-card/card-part";
import { MultiplePartsCard } from "../multiple-parts-card/multiple-parts-card";
import { Text } from "../text";
import { MultiplePartsCardCollection } from "./multiple-parts-card-collection";

export default {
  title: "Multiple Parts Card Collection",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => (
  <MultiplePartsCardCollection>
    <MultiplePartsCard>
      <CardPart contentAlign="left" id="heading">
        <Heading size={2}>Student</Heading>
      </CardPart>
    </MultiplePartsCard>
    <MultiplePartsCard>
      <CardPart contentAlign="left" id="heading">
        <Heading size={2}>Student</Heading>
      </CardPart>
    </MultiplePartsCard>
  </MultiplePartsCardCollection>
);
