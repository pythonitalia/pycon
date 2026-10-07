import React from "react";
import { Tag } from "../tag";
import { TagsCollection } from "./tags-collection";

export default {
  title: "Tags Collection",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => (
  <TagsCollection>
    <Tag color="red">Tag 1</Tag>
    <Tag color="success">Tag 2</Tag>
    <Tag color="blue">Tag 3</Tag>
  </TagsCollection>
);
