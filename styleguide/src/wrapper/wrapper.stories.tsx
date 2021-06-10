import React from "react";
import { Button } from "../button/button";
import { Paragraph } from "../paragraph/paragraph";
import { Title } from "../title";
import { Wrapper } from "./wrapper";

export default {
  title: "Wrapper",
};

export const Primary = () => (
  <Wrapper>
    <Title>Title inside a wrapper</Title>

    <Paragraph>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>

    <Paragraph>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>

    <Paragraph>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>
  </Wrapper>
);

export const CenteredContent = () => (
  <Wrapper center>
    <div>
      <Button onClick={() => {}} color="pink">
        Button
      </Button>
      <Button onClick={() => {}} color="orange">
        Button 2
      </Button>
      <Button onClick={() => {}} color="purple">
        Button 3
      </Button>
    </div>
  </Wrapper>
);
