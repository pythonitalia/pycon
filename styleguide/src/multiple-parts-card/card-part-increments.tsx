import React from "react";
import { MinusIcon } from "../icons/minus";
import { Heading } from "../heading";
import { PlusIcon } from "../icons/plus";
import { SideText } from "./sidetext";
import { Action } from "./action";

type Props = {
  children: React.ReactNode;
  value: number;
  onIncrement: () => void;
  onDecrement: () => void;
};

export const CardPartIncrements = ({
  value,
  children,
  onIncrement,
  onDecrement,
}: Props) => {
  return (
    <div className="bg-milk grid grid-cols-2 md:grid-cols-cardpart-increments divide-x">
      <SideText>{children}</SideText>
      <div className="grid grid-cols-3 divide-x">
        <Action>
          <Heading size={2}>{String(value).padStart(2, "0")}</Heading>
        </Action>
        <Action button onClick={onDecrement}>
          <MinusIcon />
        </Action>
        <Action button onClick={onIncrement}>
          <PlusIcon />
        </Action>
      </div>
    </div>
  );
};
