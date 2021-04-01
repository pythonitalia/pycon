module.exports = (componentName) => ({
  content: `
import React from "react";
import { render } from "@testing-library/react";

import { ${componentName} } from "./${componentName}";

describe("Test Component", () => {
  let props;

  beforeEach(() => {
    props = {
      foo: "bar"
    };
  });

  const renderComponent = () => render(<${componentName} {...props} />);

  it("should render foo text correctly", () => {
    props.foo = "harvey was here";
    const { getByTestId } = renderComponent();

    const component = getByTestId("${componentName}");

    expect(component).toHaveTextContent("harvey was here");
  });
});
`.trim(),
  extension: `.test.tsx`,
});
