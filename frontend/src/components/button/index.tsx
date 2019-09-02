import { Button as FannyButton, ButtonProps } from "fannypack";
import React from "react";

export const Button = (props: ButtonProps) => (
  <FannyButton {...props}>{props.children}</FannyButton>
);
