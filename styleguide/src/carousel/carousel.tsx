import React, { useState } from "react";
import { Title } from "../title";

type Props = {
  title: string;
  children: React.ReactNode;
};

const LeftArrow = () => (
  <svg width="46" height="53" viewBox="0 0 46 53">
    <path
      d="M3.63709e-07 26.5L45.75 0.086228L45.75 52.9138L3.63709e-07 26.5Z"
      fill="black"
    />
    <path
      d="M3.63709e-07 26.5L45.75 0.086228L45.75 52.9138L3.63709e-07 26.5Z"
      stroke="black"
    />
  </svg>
);

const RightArrow = () => (
  <svg width="46" height="53" viewBox="0 0 46 53">
    <path d="M46 26.5L0.249998 52.9138L0.25 0.0862235L46 26.5Z" fill="black" />
    <path
      d="M46 26.5L0.249998 52.9138L0.25 0.0862235L46 26.5Z"
      stroke="black"
    />
  </svg>
);

export const Carousel = ({ title, children }: Props) => {
  const [currentX, setCurrentX] = useState(0);

  return (
    <div>
      <div className="border-black border-b-4">
        <div className="max-w-7xl mx-auto pt-8">
          <Title>{title}</Title>
        </div>
      </div>
      <div className="max-w-7xl mx-auto flex-1 w-full relative">
        <button
          className="flex justify-center items-center absolute h-full px-16 -left-44 top-0 focus:outline-none"
          onClick={() => setCurrentX(currentX + 25)}
        >
          <LeftArrow />
        </button>

        <div className="w-full overflow-hidden border-black border-l-4">
          <div
            className="flex transform transition-transform"
            style={{ "--tw-translate-x": `${currentX}%` } as any}
          >
            {React.Children.map(children, (child) => {
              return (
                <div className="w-1/4 flex-shrink-0">
                  <div className="aspect-w-1 aspect-h-1 border-r-4 border-black">
                    {child}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <button
          className="flex justify-center items-center absolute h-full px-16 -right-44 top-0 focus:outline-none"
          onClick={() => setCurrentX(currentX - 25)}
        >
          <RightArrow />
        </button>
      </div>
    </div>
  );
};
