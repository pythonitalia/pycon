import React from "react";
import { Button } from "../button";
import { Heading } from "../heading";
import { BottomBar } from "./bottom-bar";

export const Primary = () => {
  return (
    <div className="py-6">
      <div className=" h-256">long content</div>
      <div className=" h-256">long content</div>
      <div className=" h-256">long content</div>
      <BottomBar action={<Button variant="secondary">Checkout</Button>}>
        <Heading size="display2">€ 630</Heading>
      </BottomBar>
      <div className=" h-256">content below</div>
      <div className=" h-256">content below</div>
      <div className=" h-256">content below</div>
    </div>
  );
};

export default {
  title: "Bottom bar",
};
