import React from "react";
import { Separator } from "../separator";

type Props = {
  children: React.ReactNode;
  startSeparator?: boolean;
  endSeparator?: boolean;
};

export const Page = ({
  children,
  startSeparator = true,
  endSeparator = true,
}: Props) => (
  <div>
    {startSeparator && <Separator />}
    <div className="divide-y-3">{children}</div>
    {endSeparator && <Separator />}
  </div>
);
