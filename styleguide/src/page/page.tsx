import React from "react";
import { Separator } from "../separator";

type Props = React.PropsWithChildren<{
  endSeparator?: boolean;
}>;

export const Page = ({ children, endSeparator = true }: Props) => (
  <div>
    <Separator />
    <div className="divide-y-3">{children}</div>
    {endSeparator && <Separator />}
  </div>
);
