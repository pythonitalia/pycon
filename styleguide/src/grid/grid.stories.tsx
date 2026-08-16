import React from "react";
import { Heading } from "../heading";
import { Container } from "../container";
import { Text } from "../text";
import { Grid } from "./grid";
import { GridColumn } from "./grid-column";

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

export const SpanColumns = () => {
  return (
    <Container>
      <Grid cols={12}>
        <GridColumn colSpan={4} rowSpan={2}>
          <div className="bg-purple h-full">1</div>
        </GridColumn>
        <GridColumn colSpan={8}>
          <div className="bg-green">2</div>
        </GridColumn>
        <GridColumn colSpan={1}>
          <div className="bg-yellow">3</div>
        </GridColumn>
        <GridColumn colSpan={1}>
          <div className="bg-pink">4</div>
        </GridColumn>
        <GridColumn colSpan={1}>
          <div className="bg-red">5</div>
        </GridColumn>
        <GridColumn colSpan={1}>
          <div className="bg-blue">6</div>
        </GridColumn>
      </Grid>
    </Container>
  );
};

export const DividerTest = () => {
  return (
    <div className="p-6">
      <Grid cols={2} gap="none" divide={true}>
        <div>
          <Text size="label3">From</Text>
          <Heading size={2}>300</Heading>
        </div>
        <div>
          <Text size="label3">To</Text>
          <Heading size={2}>400</Heading>
        </div>
      </Grid>
    </div>
  );
};
