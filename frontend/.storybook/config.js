import { configure } from "@storybook/react";

function loadStories() {
  require("../src/stories/index.tsx");
}

configure(loadStories, module);
