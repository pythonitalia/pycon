import React from "react";
import { SnakeCouple } from "./snake-couple";
import { SnakeDNA } from "./snake-dna";

export default {
  title: "Illustrations",
};

const Template = ({ component: Component }) => {
  return <Component />;
};
Template.args = { component: SnakeCouple };

export const SnakeCoupleStory = Template.bind({});
SnakeCoupleStory.args = { component: SnakeCouple };

export const SnakeDNAStory = Template.bind({});
SnakeDNAStory.args = { component: SnakeDNA };
