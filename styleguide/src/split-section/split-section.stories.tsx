import React from "react";
import { SplitSection } from "./split-section";

export default {
  title: "SplitSection",
};

export const Standard = () => (
  <SplitSection title="The speakers">
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
