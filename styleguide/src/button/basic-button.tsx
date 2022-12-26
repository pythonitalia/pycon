import clsx from "clsx";
import React from "react";
import { Text } from "../text";

type Props = {
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
};

export const BasicButton = ({ children, disabled, onClick }: Props) => {
  return (
    <button
      className={clsx("text-black transition-all underline-offset-8", {
        "cursor-not-allowed opacity-30": disabled,
        "hover:text-green": !disabled,
      })}
      onClick={onClick}
    >
      <Text
        color="none"
        size="label3"
        decoration="underline"
        uppercase
        weight="strong"
      >
        {children}
      </Text>
    </button>
  );
};
