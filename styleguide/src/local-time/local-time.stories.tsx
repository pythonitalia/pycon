import React from "react";

import { LocalTime } from "./local-time";

export default {
  title: "Local Time",
};

export const Primary = () => (
  <div>
    <div>
      <LocalTime datetime={new Date()} format="just-time" />
    </div>
    <div>
      <LocalTime datetime={new Date()} format="full" />
    </div>
  </div>
);
