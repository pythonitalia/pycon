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
};

export const SliderGrid = ({
  children,
  cols,
  mdCols = cols,
  title,
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

      <Container noPadding className="md:pr-4 md:pl-4">
        {useSnakeBackground && (
          <SnakeHead className="relative -rotate-90 md:rotate-0 ml-auto w-32 lg:w-52 md:mr-12 -mt-20 lg:-mt-36 hidden md:block" />
        )}

        <div
          ref={scrollerRef}
          className={clsx(
            `snap-x snap-mandatory overflow-x-auto flex md:grid md:gap-6 lg:gap-6 auto-rows-fr`,
            {
              "lg:grid-cols-1": cols === 1,
              "lg:grid-cols-2": cols === 2,
              "lg:grid-cols-3": cols === 3,
              "lg:grid-cols-4": cols === 4,
              "lg:grid-cols-5": cols === 5,
              "lg:grid-cols-6": cols === 6,
              "lg:grid-cols-7": cols === 7,
              "lg:grid-cols-8": cols === 8,
              "lg:grid-cols-9": cols === 9,
              "lg:grid-cols-10": cols === 10,
              "lg:grid-cols-11": cols === 11,
              "lg:grid-cols-12": cols === 12,

              "md:grid-cols-1": mdCols === 1,
              "md:grid-cols-2": mdCols === 2,
              "md:grid-cols-3": mdCols === 3,
              "md:grid-cols-4": mdCols === 4,
              "md:grid-cols-5": mdCols === 5,
              "md:grid-cols-6": mdCols === 6,
              "md:grid-cols-7": mdCols === 7,
              "md:grid-cols-8": mdCols === 8,
              "md:grid-cols-9": mdCols === 9,
              "md:grid-cols-10": mdCols === 10,
              "md:grid-cols-11": mdCols === 11,
              "md:grid-cols-12": mdCols === 12,
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
                "pl-2 pr-2 md:pr-0 md:pl-0"
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
