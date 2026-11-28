import React from "react";
import { Spacer } from "../spacer";
import { BasicButton } from "./basic-button";
import { Button } from "./button";

export default {
  title: "Button",
};

export const Story = ({ text, size, disabled, variant }) => (
  <div>
    <div>
      <Button onClick={() => {}} disabled={disabled} variant={variant}>
        {text}
      </Button>
    </div>
    <div>
      <Button onClick={() => {}} fullWidth disabled={disabled} variant={variant}>
        {text} - Full width
      </Button>
    </div>
    <div>
      <Button
        onClick={() => {}}
        fullWidth="mobile"
        disabled={disabled}
        variant={variant}
      >
        {text} - Full width mobile
      </Button>
    </div>
  </div>
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
  variant: {
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
      <Button onClick={() => {}} disabled={false} variant="primary">
        Primary
      </Button>
      <Spacer size="large" />
      <Button onClick={() => {}} disabled={false} variant="secondary">
        Secondary
      </Button>
      <Button
        background="red"
        onClick={() => {}}
        disabled={false}
        variant="secondary"
      >
        Secondary [custom bg]
      </Button>
      <Spacer size="large" />
      <Button onClick={() => {}} disabled={false} variant="alert">
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
