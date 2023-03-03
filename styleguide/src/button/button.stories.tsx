import React from "react";
import { Button } from "./button";
import { BasicButton } from "./basic-button";
import { Spacer } from "../spacer";

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
      <Spacer size="large" />
      <Button onClick={() => {}} disabled={false} role="secondary">
        Secondary
      </Button>
      <Button
        background="red"
        onClick={() => {}}
        disabled={false}
        role="secondary"
      >
        Secondary [custom bg]
      </Button>
      <Spacer size="large" />
      <Button onClick={() => {}} disabled={false} role="alert">
        Alert
      </Button>
    </>
  );
};

export const AsLink = () => {
  return <Button href="/test">Link Body</Button>;
};

export const BasicButtonStory = ({ disabled }) => {
  return (
    <div className="p-6">
      <BasicButton disabled={disabled}>Simple button</BasicButton>
      <Spacer size="large" />
      <BasicButton href="/test" disabled={disabled}>
        Simple button as Link
      </BasicButton>
    </div>
  );
};

BasicButtonStory.argTypes = {
  disabled: {
    defaultValue: false,
    control: {
      type: "boolean",
    },
  },
};
