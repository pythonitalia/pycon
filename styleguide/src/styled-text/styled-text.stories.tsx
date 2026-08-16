import React from "react";
import { StyledHTMLText } from "./styled-html-text";
import { StyledText } from "./styled-text";

export default {
  title: "Styled Text",
  parameters: {
    layout: "centered",
  },
  argTypes: {
    baseTextSize: {
      control: {
        type: "select",
        options: [1, 2, 3],
      },
    },
  },
};

export const HTMLText = ({ baseTextSize }) => {
  const text = `<div><p data-block-key="i4kay">Grand Hotel Mediterraneo
  is 10Km far from Firenze Peretola (FLR) airport (also called “Amerigo Vespucci”).
  </p><p data-block-key="8kaf3">You can take tram (Line 2 - ticket: 1,50€) and from the airport you will arrive at central station (Santa Maria Novella); from there you can use the same instructions for people coming by train. As alternative you can get a taxi from the airport to the hotel (it will cost around 25€ / 30€).
  </p><p data-block-key="1pc64">
  </p><p data-block-key="95gvo">Heading tests:
  </p><p data-block-key="60ffd">
  </p><h2 data-block-key="f0er2">Heading 2</h2><h3 data-block-key="bapua">Heading 3</h3>
  <h4 data-block-key="fbh63">Heading 4</h4><p data-block-key="3edn4">
  </p><p data-block-key="oljl">numbered list test:
  </p><ol><li data-block-key="aqrv0">numbered</li><li data-block-key="3ekkj">list</li></ol><p data-block-key="8a1mr">
  </p><p data-block-key="8p4ap">link test:
  </p><p data-block-key="emqre"><a href="https://google.it">link to google</a>
  </p><p data-block-key="6ct0m">An alternative airport is <b>Galileo Galilei - Pisa (PSA)</b>, 80 Km far from Florence. From there you have:
  </p><ul><li data-block-key="6u4u">Shuttle bus to Florence: if you decide to travel by bus, Terravision operates a service from Pisa airport to Florence “Santa Maria Novella” train station. You can buy the ticket directly at Pisa airport.</li>
  <li data-block-key="b8c34">Trains to Florence: there is a direct train from Pisa airport to Pisa Centrale and from there you can take the direct train to Florence “Santa Maria Novella” train station.</li></ul></div>`;
  return <StyledHTMLText text={text} baseTextSize={baseTextSize} />;
};

export const StaticContent = ({ baseTextSize }) => {
  return (
    <StyledText baseTextSize={baseTextSize}>
      <p>Things I love:</p>
      <ul>
        <li>Sushi</li>
      </ul>
      <p>Things I hate:</p>
      <ul>
        <li>Wasabi</li>
      </ul>
    </StyledText>
  );
};
