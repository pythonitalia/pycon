import React from "react";
import { ContainerSize } from "../container/container";
import { Heading } from "../heading";
import { Page } from "../page";
import { Text } from "../text";
import { Color } from "../types";
import { Section } from "./section";

export const Standard = ({
  containerSize = "base",
  background,
}: {
  containerSize: ContainerSize;
  background: Color | "none";
}) => {
  return (
    <Section containerSize={containerSize} background={background}>
      <Heading size="display1">Section!</Heading>
    </Section>
  );
};

export const SectionInsidePage = ({
  containerSize = "base",
  background,
}: {
  containerSize: ContainerSize;
  background: Color | "none";
}) => {
  return (
    <Page>
      <Section containerSize={containerSize} background={background}>
        <Heading size="display1">Section!</Heading>
      </Section>
      <Section
        illustration="snakeHead"
        containerSize={containerSize}
        background={background}
      >
        <Heading size="display1">Section Head!</Heading>
      </Section>
      <Section
        illustration="snakeTail"
        containerSize={containerSize}
        background={background}
      >
        <Heading size="display1">Section Tail!</Heading>
        <Text>
          Induco eligo, cogito sit et officia adipisici canvallis quis commodi
          neque culpa, in neque quis trivia insula canvallis dulcis amet gratia
          abundantia legio caelum galea cogito legis impera, legis ventum gratia
          trivia bene sit legis, abundantia bene bene negotium sum medius neque
          amet in oblivio modestus bene lege minim, virtus legio impera
          abundantia sit dulcis in medius eligo. Induco eligo, cogito sit et
          officia adipisici canvallis quis commodi neque culpa, in neque quis
          trivia insula canvallis dulcis amet gratia abundantia legio caelum
          galea cogito legis impera, legis ventum gratia trivia bene sit legis,
          abundantia bene bene negotium sum medius neque amet in oblivio
          modestus bene lege minim, virtus legio impera abundantia sit dulcis in
          medius eligo.
        </Text>
      </Section>
      <Section
        illustration="snakeLongNeck"
        containerSize={containerSize}
        background={background}
      >
        <Heading size="display1">Long neck illustration</Heading>
        <Text>
          Induco eligo, cogito sit et officia adipisici canvallis quis commodi
          neque culpa, in neque quis trivia insula canvallis dulcis amet gratia
          abundantia legio caelum galea cogito legis impera, legis ventum gratia
          trivia bene sit legis, abundantia bene bene negotium sum medius neque
          amet in oblivio modestus bene lege minim, virtus legio impera
          abundantia sit dulcis in medius eligo. Induco eligo, cogito sit et
          officia adipisici canvallis quis commodi neque culpa, in neque quis
          trivia insula canvallis dulcis amet gratia abundantia legio caelum
          galea cogito legis impera, legis ventum gratia trivia bene sit legis,
          abundantia bene bene negotium sum medius neque amet in oblivio
          modestus bene lege minim, virtus legio impera abundantia sit dulcis in
          medius eligo.
        </Text>
      </Section>
    </Page>
  );
};

export default {
  title: "Section",
  component: Standard,
  argTypes: {
    containerSize: {
      control: {
        type: "select",
        options: ["base", "medium"],
      },
      defaultValue: "base",
    },
    background: {
      defaultValue: "none",
      control: {
        type: "select",
        options: [
          "none",
          "coral",
          "caramel",
          "cream",
          "yellow",
          "green",
          "purple",
          "pink",
          "blue",
          "red",
          "success",
          "warning",
          "neutral",
          "black",
          "grey",
          "white",
          "milk",
        ],
      },
    },
  },
};
