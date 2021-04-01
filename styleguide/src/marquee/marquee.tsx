import React from "react";
import clsx from "clsx";

type Props = {
  children: React.ReactNode;
  bottomBorder?: boolean;
};

export const Marquee = ({ children, bottomBorder = true }: Props) => (
  <div
    className={clsx("border-t-4 border-black", {
      "border-b-4": bottomBorder,
    })}
  >
    <div className="motion-safe:animate-marquee p-8 text-3xl whitespace-nowrap">
      <div className="inline-block">{children}</div>

      {new Array(20).fill(null).map((_, index) => (
        <div key={index} className="inline-block ml-4 not-sr-only">
          /{" "}
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
