import React from "react";
import { Separator } from "../separator";

export const SectionsWrapper = ({ children }: React.PropsWithChildren<{}>) => (
  <div>
    <Separator />
    <div className="divide-y-3">{children}</div>
    <Separator />
  </div>
);
