import React from "react";
import clsx from "clsx";

type Props = {
  children: React.ReactNode;
  speed?: "slow" | "medium";
  separator?: string | React.ReactNode;
};

export const Marquee = ({
  children,
  speed = "medium",
  separator = "/",
}: Props) => (
  <div className="overflow-hidden w-full">
    <div
      className={clsx("p-8 text-lg whitespace-nowrap", {
        "motion-safe:animate-marquee-slow": speed === "slow",
        "motion-safe:animate-marquee-medium": speed === "medium",
      })}
    >
      <div className="inline-block whitespace-nowrap">{children}</div>

      {new Array(20).fill(null).map((_, index) => (
        <div
          key={index}
          className="inline-block ml-4 not-sr-only whitespace-nowrap"
        >
          <span className="inline-block mr-4">{separator}</span>
          {React.Children.map(children, (child) => {
            if (React.isValidElement(child)) {
              return React.cloneElement(child);
            }

            return child;
          })}
        </div>
      ))}
    </div>
  </div>
);
