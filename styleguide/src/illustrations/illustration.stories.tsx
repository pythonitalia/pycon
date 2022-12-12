import React from "react";
import { SnakeCouple } from "./snake-couple";
import { SnakeDNA } from "./snake-dna";
import { Snake1 } from "./snake-1";
import { Snake2 } from "./snake-2";
import { SnakeTail } from "./snake-tail";
import { Snake4 } from "./snake-4";
import { Snake5 } from "./snake-5";
import { Cathedral } from "./cathedral";
import { Florence } from "./florence";
import { TripleSnakes } from "./triple-snakes";

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

export const Snake1Story = Template.bind({});
Snake1Story.args = { component: Snake1 };

export const Snake2Story = Template.bind({});
Snake2Story.args = { component: Snake2 };

export const Snake3Story = Template.bind({});
Snake3Story.args = { component: SnakeTail };

export const Snake4Story = Template.bind({});
Snake4Story.args = { component: Snake4 };

export const Snake5Story = Template.bind({});
Snake5Story.args = { component: Snake5 };

export const CathedralStory = Template.bind({});
CathedralStory.args = { component: Cathedral };

export const FlorenceStory = Template.bind({});
FlorenceStory.args = { component: Florence };

export const TripleSnakesStory = Template.bind({});
TripleSnakesStory.args = { component: TripleSnakes };
