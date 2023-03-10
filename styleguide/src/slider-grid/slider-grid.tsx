import clsx from "clsx";
import React, { useEffect, useRef } from "react";
import { Container } from "../container";
import { Heading } from "../heading";
import { SnakeBody } from "../illustrations/snake-body";
import { SnakeHead } from "../illustrations/snake-head";
import { SnakeTail } from "../illustrations/snake-tail";
import { Spacer } from "../spacer";

type Props = {
  children: React.ReactNode;
  cols: number;
  mdCols?: number;
  title?: string | React.ReactNode;
  background?: "snake" | "none";
  justifyContent?: "center";
  wrap?: "wrap" | "nowrap";
};

export const SliderGrid = ({
  children,
  cols,
  mdCols = cols,
  title,
  wrap = "wrap",
  justifyContent,
  background = "none",
}: Props) => {
  const scrollerRef = useRef<HTMLDivElement>(null);
  const listItemsRef = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    if (!scrollerRef) {
      return;
    }

    const callback = (entries: IntersectionObserverEntry[]) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("grid-section--current-item");
        } else {
          entry.target.classList.remove("grid-section--current-item");
        }
      });
    };

    const observer = new IntersectionObserver(callback, {
      root: scrollerRef.current,
      rootMargin: "0px",
      threshold: 0.75,
    });

    listItemsRef.current.forEach((item) => {
      if (item) {
        item.classList.add("grid-section--item");
        observer.observe(item);
      }
    });

    return () => {
      observer.disconnect();
    };
  }, []);

  const countChildren = React.Children.count(children);
  const useSnakeBackground = background === "snake";

  return (
    <div className="slider-grid">
      {title && (
        <>
          <Container>
            <Heading size="display2">{title}</Heading>
          </Container>
          <Spacer size="xl" />
        </>
      )}

      <Container noPadding>
        {useSnakeBackground && (
          <SnakeHead className="relative -rotate-90 md:rotate-0 ml-auto w-32 lg:w-52 md:mr-12 -mt-20 lg:-mt-36 hidden md:block" />
        )}

        <div
          ref={scrollerRef}
          className={clsx(
            `snap-x snap-mandatory overflow-x-auto flex md:-mt-2 lg:-mt-4 md:px-2 lg:px-0`,
            {
              "md:justify-center": justifyContent === "center",

              "md:flex-wrap": wrap === "wrap",
              "md:flex-nowrap": wrap === "nowrap",
            }
          )}
        >
          <div className="pl-2 md:hidden"></div>
          {React.Children.map(children, (child, index) => (
            <div
              ref={(el) => (listItemsRef.current[index] = el)}
              className={clsx(
                "md:opacity-100 z-10 transition-opacity snap-center shrink-0",
                "w-scroller-item md:w-auto relative",
                "pl-2 pr-2 md:min-w-0 md:p-2 lg:p-4",
                {
                  "lg:basis-[calc((100%/1))]": cols === 1,
                  "lg:basis-[calc((100%/2))]": cols === 2,
                  "lg:basis-[calc((100%/3))]": cols === 3,
                  "lg:basis-[calc((100%/4))]": cols === 4,
                  "lg:basis-[calc((100%/5))]": cols === 5,
                  "lg:basis-[calc((100%/6))]": cols === 6,
                  "lg:basis-[calc((100%/7))]": cols === 7,
                  "lg:basis-[calc((100%/8))]": cols === 8,
                  "lg:basis-[calc((100%/9))]": cols === 9,
                  "lg:basis-[calc((100%/10))]": cols === 10,
                  "lg:basis-[calc((100%/11))]": cols === 11,
                  "lg:basis-[calc((100%/12))]": cols === 12,

                  "md:basis-[calc((100%/1))]": mdCols === 1,
                  "md:basis-[calc((100%/2))]": mdCols === 2,
                  "md:basis-[calc((100%/3))]": mdCols === 3,
                  "md:basis-[calc((100%/4))]": mdCols === 4,
                  "md:basis-[calc((100%/5))]": mdCols === 5,
                  "md:basis-[calc((100%/6))]": mdCols === 6,
                  "md:basis-[calc((100%/7))]": mdCols === 7,
                  "md:basis-[calc((100%/8))]": mdCols === 8,
                  "md:basis-[calc((100%/9))]": mdCols === 9,
                  "md:basis-[calc((100%/10))]": mdCols === 10,
                  "md:basis-[calc((100%/11))]": mdCols === 11,
                  "md:basis-[calc((100%/12))]": mdCols === 12,
                }
              )}
            >
              {useSnakeBackground &&
                index !== countChildren - 1 &&
                index % cols !== cols - 1 && (
                  <SnakeBody className="absolute w-52 lg:w-96 left-1/2 translate-x-5 -z-1 top-[10%] hidden md:block" />
                )}
              {child}
            </div>
          ))}
          <div className="pr-2 md:hidden"></div>
        </div>

        {useSnakeBackground && (
          <SnakeTail className="w-32 lg:w-52 md:ml-12 -mt-20 relative block -rotate-90 md:rotate-0" />
        )}
      </Container>
    </div>
  );
};
