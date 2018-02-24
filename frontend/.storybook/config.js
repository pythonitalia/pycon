import { configure } from "@storybook/react";

import 'modern-normalize';

function loadStories() {
  require("../src/stories/index.tsx");
  require("../src/stories/navbar/index.tsx");
  require("../src/stories/logo/index.tsx");
}

configure(loadStories, module);
