module.exports = (componentName) => ({
  content: `
import React from "react";

export const ${componentName} = () => (
    <div>Hello</div>
);
`.trim(),
  extension: `.tsx`,
});
