import React from "react";
import { Grid } from "./grid";

export default {
  title: "Grid",
  argTypes: {
    cols: {
      defaultValue: 3,
      control: {
        type: "number",
      },
    },
  },
};

export const Primary = ({ cols }) => {
  return (
    <div className="p-6">
      <Grid cols={cols}>
        <div className="bg-purple">1</div>
        <div className="bg-green">2</div>
        <div className="bg-pink">3</div>
        <div className="bg-blue">4</div>
        <div className="bg-red">5</div>
        <div className="bg-yellow">6</div>
      </Grid>
    </div>
  );
};
