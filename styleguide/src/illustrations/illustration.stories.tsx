import React from "react";
import { Cathedral } from "./cathedral";
import { Florence } from "./florence";
import { Florence2 } from "./florence2";
import { HandWithSnakeInside } from "./hand-with-snake-inside";
import { Snake1 } from "./snake-1";
import { Snake2 } from "./snake-2";
import { Snake4 } from "./snake-4";
import { Snake5 } from "./snake-5";
import { SnakeBody } from "./snake-body";
import { SnakeCouple } from "./snake-couple";
import { SnakeDNA } from "./snake-dna";
import { SnakeHead } from "./snake-head";
import { SnakeInDragon } from "./snake-in-dragon";
import { SnakeInDragonInverted } from "./snake-in-dragon-inverted";
import { SnakeLetter } from "./snake-letter";
import { SnakeLongNeck } from "./snake-long-neck";
import { SnakePencil } from "./snake-pencil";
import { SnakeTail } from "./snake-tail";
import { SnakeWithBalloon } from "./snake-with-balloon";
import { SnakeWithContacts } from "./snake-with-contacts";
import { SnakesWithBanner } from "./snakes-with-banner";
import { SnakesWithCocktail } from "./snakes-with-cocktail";
import { SnakesWithDirections } from "./snakes-with-directions";
import { SnakesWithOutlines } from "./snakes-with-outlines";
import { TripleSnakes } from "./triple-snakes";

export default {
  title: "Illustrations",
};

const Template = ({ component: Component }) => {
  return <Component />;
};
Template.args = { component: SnakeCouple };

export const CathedralStory = Template.bind({});
CathedralStory.args = { component: Cathedral };

export const FlorenceStory = Template.bind({});
FlorenceStory.args = { component: Florence };

export const Florence2Story = Template.bind({});
Florence2Story.args = { component: Florence2 };

export const HandWithSnakeInsideStory = Template.bind({});
HandWithSnakeInsideStory.args = { component: HandWithSnakeInside };

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

export const SnakeBodyStory = Template.bind({});
SnakeBodyStory.args = { component: SnakeBody };

export const SnakeCoupleStory = Template.bind({});
SnakeCoupleStory.args = { component: SnakeCouple };

export const SnakeDNAStory = Template.bind({});
SnakeDNAStory.args = { component: SnakeDNA };

export const SnakeHeadStory = Template.bind({});
SnakeHeadStory.args = { component: SnakeHead };

export const SnakeInDragonInvertedStory = Template.bind({});
SnakeInDragonInvertedStory.args = { component: SnakeInDragonInverted };

export const SnakeInDragonStory = Template.bind({});
SnakeInDragonStory.args = { component: SnakeInDragon };

export const SnakeLetterStory = Template.bind({});
SnakeLetterStory.args = { component: SnakeLetter };

export const SnakeLongNeckStory = Template.bind({});
SnakeLongNeckStory.args = { component: SnakeLongNeck };

export const SnakePencilStory = Template.bind({});
SnakePencilStory.args = { component: SnakePencil };

export const SnakeTailStory = Template.bind({});
SnakeTailStory.args = { component: SnakeTail };

export const SnakeWithBalloonStory = Template.bind({});
SnakeWithBalloonStory.args = { component: SnakeWithBalloon };

export const SnakeWithContactsStory = Template.bind({});
SnakeWithContactsStory.args = { component: SnakeWithContacts };

export const SnakesWithBannerStory = Template.bind({});
SnakesWithBannerStory.args = { component: SnakesWithBanner };

export const SnakesWithCocktailStory = Template.bind({});
SnakesWithCocktailStory.args = { component: SnakesWithCocktail };

export const SnakesWithDirectionsStory = Template.bind({});
SnakesWithDirectionsStory.args = { component: SnakesWithDirections };

export const SnakesWithOutlinesStory = Template.bind({});
SnakesWithOutlinesStory.args = { component: SnakesWithOutlines };

export const TripleSnakesStory = Template.bind({});
TripleSnakesStory.args = { component: TripleSnakes };
