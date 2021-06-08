import React from "react";
import { SplitSection } from "./split-section";

export const Standard = ({ ...props }) => (
  <SplitSection title="The speakers" {...props}>
    <p className="font-bold text-purple-600 mb-8">
      Lorem ipsum dolor sit, amet consectetur adipisicing elit.
    </p>
    <p>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Eius delectus
      velit temporibus facilis quis dolore sit fugit vel labore, ut odit
      perspiciatis id, vitae maiores? Sequi cupiditate soluta officia
      voluptatem?
    </p>
  </SplitSection>
);

export default {
  title: "SplitSection",
  component: Standard,
  argTypes: {
    illustrationFirst: {
      control: {
        type: "boolean",
      },
    },
  },
};
