import React from "react";
import { MinusIcon } from "../icons/minus";
import { PlusIcon } from "../icons/plus";
import { Action } from "./action";
import { SideText } from "./sidetext";

type Props = {
  children: React.ReactNode;
  action: "add" | "remove";
  onAdd?: () => void;
  onRemove?: () => void;
};

export const CardPartAddRemove = ({
  children,
  action,
  onAdd,
  onRemove,
}: Props) => {
  return (
    <div className="bg-milk grid grid-cols-bottombar">
      <SideText>{children}</SideText>
      <div className="grid border-l">
        {action === "add" && (
          <Action button onClick={onAdd}>
            <PlusIcon />
          </Action>
        )}
        {action === "remove" && (
          <Action button negative onClick={onRemove}>
            <MinusIcon />
          </Action>
        )}
      </div>
    </div>
  );
};
