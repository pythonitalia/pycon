import React from "react";
import { Button } from "./button";

export default {
  title: "Button",
};

export const Story = ({ text, size, disabled, role }) => (
  <>
    <Button onClick={() => {}} disabled={disabled} role={role}>
      {text}
    </Button>
  </>
);

Story.argTypes = {
  text: {
    defaultValue: "Button",
    control: {
      type: "text",
    },
  },
  disabled: {
    defaultValue: false,
    control: {
      type: "boolean",
    },
  },
  role: {
    defaultValue: "primary",
    control: {
      type: "select",
      options: ["primary", "secondary"],
    },
  },
};

export const AllButtons = () => {
  return (
    <>
      <Button onClick={() => {}} disabled={false} role="primary">
        Primary
      </Button>
      <Button onClick={() => {}} disabled={false} role="secondary">
        Secondary
      </Button>
    </>
  );
};

export const AsLink = () => {
  return <Button linkTo="/test">Link Body</Button>;
};
