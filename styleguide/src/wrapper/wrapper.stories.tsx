import React from "react";
import { Paragraph } from "../paragraph/paragraph";
import { Heading } from "../heading";
import { Wrapper } from "./wrapper";

export default {
  title: "Wrapper",
};

export const Primary = () => (
  <Wrapper>
    <Heading>Title inside a wrapper</Heading>

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
