import clsx from "clsx";
import React, { useEffect, useRef } from "react";
import { Container } from "../container";
import { Heading } from "../heading";
import { SnakeBody } from "../illustrations/snake-body";
import { SnakeHead } from "../illustrations/snake-head";
import { SnakeTail } from "../illustrations/snake-tail";
import { Spacer } from "../spacer";

type Props = React.PropsWithChildren<{
  cols: number;
  title: string | React.ReactNode;
  background?: "snake" | "none";
}>;

export const SliderGrid = ({
  children,
  cols,
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
      <Container>
        <Heading size="display2">{title}</Heading>
      </Container>
      <Spacer size="xl" />

      <Container noPadding>
        {useSnakeBackground && (
          <SnakeHead className="relative -rotate-90 md:rotate-0 ml-auto w-32 lg:w-52 md:mr-12 -mt-20 lg:-mt-36 hidden md:block" />
        )}

        <div
          ref={scrollerRef}
          className={clsx(
            `snap-x snap-mandatory overflow-x-auto flex md:grid md:gap-0 lg:gap-6 auto-rows-fr`,
            {
              "md:grid-cols-1": cols === 1,
              "md:grid-cols-2": cols === 2,
              "md:grid-cols-3": cols === 3,
              "md:grid-cols-4": cols === 4,
              "md:grid-cols-5": cols === 5,
            }
          )}
        >
          {React.Children.map(children, (child, index) => (
            <div
              ref={(el) => (listItemsRef.current[index] = el)}
              className="md:opacity-100 z-10 transition-opacity snap-center shrink-0 w-scroller-item pl-2 pr-2 first:pl-4 last:pr-4 md:w-auto relative"
            >
              {useSnakeBackground &&
                index !== countChildren - 1 &&
                index % cols !== cols - 1 && (
                  <SnakeBody className="absolute w-52 lg:w-96 left-1/2 translate-x-5 -z-1 top-[10%] hidden md:block" />
                )}
              {child}
            </div>
          ))}
        </div>

        {useSnakeBackground && (
          <SnakeTail className="w-32 lg:w-52 md:ml-12 -mt-20 relative block -rotate-90 md:rotate-0" />
        )}
      </Container>
    </div>
  );
};
