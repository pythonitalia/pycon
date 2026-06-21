import React from "react";
import TextTransition, { presets } from "react-text-transition";

export const IntermissionText = ({ children }: { children: string }) => (
  <div className="text-7xl font-bold text-white">
    <TextTransition text={children} springConfig={presets.wobbly} />
  </div>
);
