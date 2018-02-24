import { configure } from "@storybook/react";

import 'modern-normalize';

function loadStories() {
  require("../src/stories/index.tsx");
  require("../src/stories/navbar/index.tsx");
}

configure(loadStories, module);
