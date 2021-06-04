import React from "react";

import { Paragraph } from "./paragraph";

export default {
  title: "Paragrah",
};

export const Primary = () => (
  <div>
    <Paragraph>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>

    <Paragraph bold>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>

    <Paragraph bold color="purple">
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Doloribus vero
      saepe adipisci rerum, itaque minima voluptas quasi porro eius accusamus
      quo aspernatur laborum nam enim. Iusto iure doloribus molestias et.
    </Paragraph>
  </div>
);
