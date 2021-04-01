module.exports = (componentName) => ({
  content: `
import React from "react";
import { ${componentName} } from "./${componentName}";

export default {
    title: "${componentName}"
};

export const Story = () => <${componentName} />;
`.trim(),
  extension: `.stories.tsx`,
});
