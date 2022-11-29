import React from "react";
import { GithubIcon } from "../icons/github";
import { TwitterIcon } from "../icons/twitter";
import { Button } from "./button";

export default {
  title: "Button",
};

export const Story = () => (
  <>
    <div className="mb-4">
      <Button onClick={() => {}} color="black">
        🐙 Login with GitHub
      </Button>
    </div>
    <div>
      <Button onClick={() => {}} color="blue">
        🐦 Login with Twitter
      </Button>
    </div>
  </>
);

export const WithIcon = () => (
  <>
    <div className="mb-4">
      <Button
        icon={<GithubIcon fill="white" />}
        onClick={() => {}}
        color="black"
      >
        Login with GitHub
      </Button>
    </div>
    <div>
      <Button
        icon={<TwitterIcon fill="white" />}
        onClick={() => {}}
        color="blue"
      >
        Login with Twitter
      </Button>
    </div>
  </>
);
