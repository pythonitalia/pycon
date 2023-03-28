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
import { SnakeTailUp } from "./snake-tail-up";
import { SnakeWithBalloon } from "./snake-with-balloon";
import { SnakeWithContacts } from "./snake-with-contacts";
import { SnakesWithBanner } from "./snakes-with-banner";
import { SnakesWithCocktail } from "./snakes-with-cocktail";
import { SnakesWithDirections } from "./snakes-with-directions";
import { SnakesWithOutlines } from "./snakes-with-outlines";
import { TripleSnakes } from "./triple-snakes";
import { Illustration } from "./types";

export const getIllustration = (name: Illustration | undefined) => {
  switch (name) {
    case "cathedral":
      return Cathedral;
    case "florence":
      return Florence;
    case "florence2":
      return Florence2;
    case "handWithSnakeInside":
      return HandWithSnakeInside;
    case "snake1":
      return Snake1;
    case "snake2":
      return Snake2;
    case "snake4":
      return Snake4;
    case "snake5":
      return Snake5;
    case "snakeBody":
      return SnakeBody;
    case "snakeCouple":
      return SnakeCouple;
    case "snakeDNA":
      return SnakeDNA;
    case "snakeHead":
      return SnakeHead;
    case "snakeInDragon":
      return SnakeInDragon;
    case "snakeInDragonInverted":
      return SnakeInDragonInverted;
    case "snakeLetter":
      return SnakeLetter;
    case "snakeLongNeck":
      return SnakeLongNeck;
    case "snakePencil":
      return SnakePencil;
    case "snakeTail":
      return SnakeTail;
    case "snakeWithBalloon":
      return SnakeWithBalloon;
    case "snakeWithContacts":
      return SnakeWithContacts;
    case "snakesWithBanner":
      return SnakesWithBanner;
    case "snakesWithCocktail":
      return SnakesWithCocktail;
    case "snakesWithDirections":
      return SnakesWithDirections;
    case "snakesWithOutlines":
      return SnakesWithOutlines;
    case "tripleSnakes":
      return TripleSnakes;
    case "snakeTailUp":
      return SnakeTailUp;
  }
  return null;
};
