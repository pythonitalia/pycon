import React, { useState } from "react";
import { Title } from "../title";

type Props = {
  title: string;
  children: React.ReactNode;
};

const LeftArrow = ({ className }: { className?: string }) => (
  <svg width="46" height="53" viewBox="0 0 46 53" className={className}>
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

const RightArrow = ({ className }: { className?: string }) => (
  <svg width="46" height="53" viewBox="0 0 46 53" className={className}>
    <path d="M46 26.5L0.249998 52.9138L0.25 0.0862235L46 26.5Z" fill="black" />
    <path
      d="M46 26.5L0.249998 52.9138L0.25 0.0862235L46 26.5Z"
      stroke="black"
    />
  </svg>
);

export const Carousel = ({ title, children }: Props) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const previous = () => setCurrentIndex(Math.max(0, currentIndex - 1));
  const next = () =>
    setCurrentIndex(
      Math.min(React.Children.count(children) - 1, currentIndex + 1)
    );

  return (
    <div>
      <div className="border-black border-b-4">
        <div className="max-w-7xl mx-auto px-4 py-8 flex">
          <Title marginBottom={false}>{title}</Title>

          <div className="ml-auto flex">
            <button className="flex h-full py-4" onClick={previous}>
              <LeftArrow className="h-5" />
            </button>
            <button className="flex h-full py-4" onClick={next}>
              <RightArrow className="h-5" />
            </button>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto flex-1 w-full relative">
        <button
          className="hidden md:flex justify-center items-center absolute h-full px-16 -left-44 top-0 focus:outline-none"
          onClick={previous}
        >
          <LeftArrow />
        </button>

        <div className="w-full overflow-hidden border-black border-l-4">
          <div
            className="flex transform transition-transform"
            style={
              {
                "--current-index": currentIndex,
                // TODO: how can we change this based on the current breakpoint?
                "--per-page": 1,
                "--tw-translate-x": `calc(var(--current-index) * -100% / var(--per-page))`,
              } as any
            }
          >
            {React.Children.map(children, (child) => {
              return (
                <div className="w-full md:w-1/4 flex-shrink-0">
                  <div className="aspect-w-1 aspect-h-1 border-r-4 border-black">
                    {child}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <button
          className="hidden md:flex justify-center items-center absolute h-full px-16 -right-44 top-0 focus:outline-none"
          onClick={next}
        >
          <RightArrow />
        </button>
      </div>
    </div>
  );
};
