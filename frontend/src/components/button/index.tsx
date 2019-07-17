import React from "react";

import { Button as FannyButton, ButtonProps } from "fannypack";

export const Button = (props: ButtonProps) => (
  <FannyButton {...props}>{props.children}</FannyButton>
);
