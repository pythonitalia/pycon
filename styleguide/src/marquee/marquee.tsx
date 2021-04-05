import React from "react";

type Props = {
  children: React.ReactNode;
};

export const Marquee = ({ children }: Props) => (
  <div className="overflow-hidden w-full">
    <div className="motion-safe:animate-marquee p-8 text-3xl whitespace-nowrap">
      <div className="inline-block whitespace-nowrap">{children}</div>

      {new Array(20).fill(null).map((_, index) => (
        <div
          key={index}
          className="inline-block ml-4 not-sr-only whitespace-nowrap"
        >
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
