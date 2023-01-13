import clsx from "clsx";
import React from "react";
import { getBackgroundClasses } from "../colors-utils";
import { Container } from "../container";
import { ContainerSize } from "../container/container";
import { Spacer } from "../spacer";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  noContainer?: boolean;
  containerSize?: ContainerSize;
  background?: Color | "none";
  spacingSize?: "xl" | "xxl";
};

export const Section = ({
  children,
  noContainer = false,
  containerSize = "base",
  background = "none",
  spacingSize = "xl",
}: Props) => {
  const Wrapper = noContainer ? React.Fragment : Container;
  const wrapperProps = noContainer ? {} : { size: containerSize };
  return (
    <div
      className={clsx({
        ...getBackgroundClasses(background),

        /* this is an hack until we add tailwind to pycon :) */
        "relative ml-auto w-32 lg:w-52 mr-6 md:mr-12 -mt-36 md:-mt-24 lg:-mt-44 hidden md:block":
          false,
      })}
    >
      <Wrapper {...wrapperProps}>
        <Spacer size={spacingSize} />
        {children}
        <Spacer size={spacingSize} />
      </Wrapper>
    </div>
  );
};
