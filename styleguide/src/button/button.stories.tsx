import React from "react";
import { Button } from "./button";

export default {
  title: "Button",
};

export const Story = () => (
  <>
    <div className="mb-4">
      <Button onClick={() => {}} color="black">🐙 Login with GitHub</Button>
    </div>
    <div>
      <Button onClick={() => {}} color="aquamarine">
        🐦 Login with Twitter
      </Button>
    </div>
  </>
);
