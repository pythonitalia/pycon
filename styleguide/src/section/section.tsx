import clsx from "clsx";
import React from "react";
import { Container } from "../container";
import { ContainerSize } from "../container/container";
import { Spacer } from "../spacer";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  containerSize?: ContainerSize;
  background?: Color | "none";
};

export const Section = ({
  children,
  containerSize = "base",
  background = "none",
}: Props) => {
  return (
    <div
      className={clsx({
        "bg-coral": background === "coral",
        "bg-caramel": background === "caramel",
        "bg-cream": background === "cream",
        "bg-yellow": background === "yellow",
        "bg-green": background === "green",
        "bg-purple": background === "purple",
        "bg-pink": background === "pink",
        "bg-blue": background === "blue",
        "bg-red": background === "red",
        "bg-success": background === "success",
        "bg-warning": background === "warning",
        "bg-neutral": background === "neutral",
        "bg-black": background === "black",
        "bg-grey": background === "grey",
        "bg-white": background === "white",
        "bg-milk": background === "milk",
      })}
    >
      <Container size={containerSize}>
        <Spacer size="xl" />
        {children}
        <Spacer size="xl" />
      </Container>
    </div>
  );
};
