import clsx from "clsx";
import React from "react";
import { Text } from "../text";

type Props = {
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: (
    e: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>
  ) => void;
  href?: string;
  target?: string;
  rel?: string;
};

export const BasicButton = ({
  children,
  disabled,
  onClick,
  href,
  target,
  rel,
}: Props) => {
  const Component = href ? "a" : "button";
  return (
    <Component
      className={clsx(
        "text-black transition-all underline-offset-8 cursor-pointer",
        {
          "cursor-not-allowed opacity-30": disabled,
          "hover:text-green": !disabled,
        }
      )}
      onClick={onClick}
      target={target}
      rel={rel}
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
    </Component>
  );
};
