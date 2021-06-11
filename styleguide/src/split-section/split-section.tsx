import clsx from "clsx";
import React from "react";
import { SnakeCouple } from "../illustrations";
import { Title } from "../title";
import { Color } from "../types";

type Props = {
  title: string;
  children: React.ReactNode;
  illustration?: (props: any) => React.ReactElement;
  illustrationFirst?: boolean;
  hideIllustrationOnMobile?: boolean;
  highlightColor?: Color;
};

export const SplitSection = ({
  title,
  children,
  illustrationFirst = false,
  hideIllustrationOnMobile = false,
  illustration: Illustration = SnakeCouple,
  highlightColor = "keppel",
}: Props) => {
  let top = (
    <div className="p-8 md:p-16 md:w-1/2">
      <Title>{title}</Title>

      {children}
    </div>
  );
  let bottom = (
    <div
      className={clsx("p-8 md:p-16 relative overflow-hidden md:w-1/2", {
        hidden: hideIllustrationOnMobile,
        "md:block": hideIllustrationOnMobile,
      })}
    >
      <div className="max-w-xs">
        <div className="relative aspect-w-1 aspect-h-1">
          <div
            className={clsx("absolute w-full h-full bg-keppel top-10 left-20", {
              "bg-aquamarine": highlightColor === "aquamarine",
              "bg-casablanca": highlightColor === "casablanca",
              "bg-orange": highlightColor === "orange",
              "bg-keppel": highlightColor === "casablanca",
              "bg-pink": highlightColor === "pink",
              "bg-purple": highlightColor === "purple",
              "bg-black": highlightColor === "black",
            })}
          ></div>
          <Illustration className="w-full" />
        </div>
      </div>
    </div>
  );

  if (illustrationFirst) {
    [bottom, top] = [top, bottom];
  }

  return (
    <div>
      <div className={clsx("max-w-7xl mx-auto md:flex md:grid-cols-2 md:divide-y-0 md:divide-x-4", {
        "divide-y-4": !hideIllustrationOnMobile
      })}>
        {top}
        {bottom}
      </div>
    </div>
  );
};
