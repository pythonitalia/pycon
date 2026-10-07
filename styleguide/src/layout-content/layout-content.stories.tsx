import React from "react";
import { Spacer } from "../spacer";

import { LayoutContent } from "./layout-content";

export default {
  title: "Layout Content",
};

export const Primary = () => {
  return (
    <div className="p-6">
      <LayoutContent>Test content</LayoutContent>
      <LayoutContent showFrom="desktop">Show from Desktop</LayoutContent>
      <LayoutContent showFrom="tablet">Show from Tablet</LayoutContent>
      <LayoutContent showFrom="mobile">Show from Mobile</LayoutContent>

      <Spacer size="large" />

      <LayoutContent showUntil="desktop">Show until Desktop</LayoutContent>
      <LayoutContent showUntil="tablet">Show until Tablet</LayoutContent>
    </div>
  );
};
