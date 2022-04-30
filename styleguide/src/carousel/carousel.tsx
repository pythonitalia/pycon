import clsx from "clsx";
import React, { useEffect, useState } from "react";
import { Title } from "../title";
import { Color } from "../types";

type Props = {
  title: string;
  children: React.ReactNode;
};

const MAX_PAGE_SIZE = 4;
const MIN_PAGE_SIZE = 1;

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

const COLORS: Color[] = [
  "orange",
  "keppel",
  "casablanca",
  "aquamarine",
  "purple",
];

const ArrowButton = ({
  onClick,
  className,
  direction = "left",
}: {
  onClick: () => void;
  className: string;
  direction?: "left" | "right";
}) => (
  <button
    className={clsx(
      "hidden 2xl:flex justify-center items-center absolute h-full top-0 focus:outline-none",
      className
    )}
    onClick={onClick}
  >
    {direction === "left" ? <LeftArrow /> : <RightArrow />}
  </button>
);

export const Carousel = ({ title, children }: Props) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [pageSize, setPageSize] = useState(MAX_PAGE_SIZE);

  const totalCount = React.Children.count(children);

  const previous = () => setCurrentIndex(Math.max(0, currentIndex - 1));
  const next = () =>
    setCurrentIndex(Math.min(totalCount - pageSize, currentIndex + 1));

  useEffect(() => {
    const listener = () => {
      if (window.innerWidth >= 768) {
        const maxIndexForSize = totalCount - MAX_PAGE_SIZE;

        setPageSize(MAX_PAGE_SIZE);
        setCurrentIndex((value) =>
          value > maxIndexForSize ? maxIndexForSize : value
        );
      } else {
        setPageSize(MIN_PAGE_SIZE);
      }
    };

    listener();
    window.addEventListener("resize", listener);

    return () => {
      window.removeEventListener("resize", listener);
    };
  }, []);

  return (
    <div>
      <div className="border-y-4 border-black">
        <div className="flex px-8 py-8 mx-auto max-w-7xl">
          <Title marginBottom={false}>{title}</Title>

          <div className="flex ml-auto 2xl:hidden">
            <button
              className="flex items-center h-full py-4"
              onClick={previous}
            >
              <LeftArrow className="h-5" />
            </button>
            <button className="flex items-center h-full py-4" onClick={next}>
              <RightArrow className="h-5" />
            </button>
          </div>
        </div>
      </div>
      <div className="relative flex-1 w-full mx-auto max-w-7xl border-b-4 border-black">
        <ArrowButton onClick={previous} className="pr-16 -left-28" />

        <div className="w-full overflow-hidden border-l-4 border-black">
          <div
            className="flex transition-transform transform carousel-container"
            style={
              {
                "--current-index": currentIndex,
                "--total-count": totalCount,
              } as any
            }
          >
            {React.Children.map(children, (child, index) => (
              <div className="flex-shrink-0 w-full md:w-1/4">
                <div className="border-r-4 border-black aspect-w-1 aspect-h-1">
                  {React.cloneElement(child as React.ReactElement, {
                    className: `bg-${COLORS[index % COLORS.length]}`,
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
        <ArrowButton
          onClick={next}
          className="pl-16 -right-28"
          direction="right"
        />
      </div>
    </div>
  );
};
