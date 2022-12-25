import React from "react";
import { Text } from "../text";

type Props = {
  children: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
};

export const BasicButton = ({ children, onClick }: Props) => {
  return (
    <button
      className="text-black hover:text-green transition-colors underline-offset-8"
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
