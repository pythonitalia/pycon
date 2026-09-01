import React from "react";
import { Grid } from "../grid";
import { Tag } from "./tag";

export const Primary = () => {
  return (
    <Grid cols={3}>
      <Tag color="coral">coral tag</Tag>
      <Tag color="caramel">caramel tag</Tag>
      <Tag color="cream">cream tag</Tag>
      <Tag color="yellow">yellow tag</Tag>
      <Tag color="green">green tag</Tag>
      <Tag color="purple">purple tag</Tag>
      <Tag color="pink">pink tag</Tag>
      <Tag color="blue">blue tag</Tag>
      <Tag color="red">red tag</Tag>
      <Tag color="success">success tag</Tag>
      <Tag color="warning">warning tag</Tag>
      <Tag color="neutral">neutral tag</Tag>
      <Tag color="black">black tag</Tag>
      <Tag color="grey">grey tag</Tag>
      <Tag color="white">white tag</Tag>
      <Tag color="milk">milk tag</Tag>
    </Grid>
  );
};

export default {
  title: "Tag",
  parameters: {
    layout: "centered",
  },
};
