import clsx from "clsx";
import React, { useEffect, useRef } from "react";
import { Separator } from "../separator";
import { Container } from "../container";

type Props = {
  children: React.ReactNode;
  sideContent: React.ReactNode;
  sideContentBackground?: string;
  sideContentType?: "illustration" | "other";
  invert?: boolean;
  hideSideContentOnMobile?: boolean;
  sideContentPadding?: boolean;
  sideContentClassName?: string;
  className?: string;
  contentSpacing?: "even" | "medium" | "2md";
};

export const SplitSection = ({
  children,
  sideContent,
  sideContentBackground,
  sideContentType = "illustration",
  contentSpacing = "even",
  hideSideContentOnMobile = false,
  sideContentPadding = true,
  invert = false,
  className,
  sideContentClassName,
}: Props) => {
  const illustrationRef = useRef<any>();
  const isIllustration = sideContentType === "illustration";
  const isOtherContent = sideContentType === "other";

  useEffect(() => {
    // Fixes a bug in safari where the svg height is not displayed correctly
    // setting intrinsic as height and then removing it fixes the issue
    if (!illustrationRef.current) {
      return;
    }

    const svgElement = illustrationRef.current.firstElementChild as SVGElement;

    svgElement.style.height = "intrinsic";
    requestAnimationFrame(() => {
      svgElement.style.height = "";
    });
  }, []);

  return (
    <div className="overflow-clip">
      <Container
        className={clsx(
          "grid",
          {
            "grid-cols-1 lg:grid-cols-2 lg:gap-10": contentSpacing === "even",

            "grid-cols-1 lg:gap-24":
              contentSpacing === "medium" || contentSpacing === "2md",

            "lg:grid-cols-[650px_max-content]":
              contentSpacing === "medium" && !invert,
            "lg:grid-cols-[max-content_650px]":
              contentSpacing === "medium" && invert,

            "lg:grid-cols-[1fr_max-content]":
              contentSpacing === "2md" && !invert,
            "lg:grid-cols-[max-content_1fr]":
              contentSpacing === "2md" && invert,
          },
          className
        )}
      >
        {/* content */}
        <div
          className={clsx("h-full", {
            "order-2 lg:order-1": !invert,
            "order-2 lg:order-2": invert,
          })}
        >
          <Separator
            escapeContainer
            hidden={hideSideContentOnMobile}
            mobileOnly={true}
          />
          <div
            className={clsx("h-full flex justify-center items-start flex-col", {
              "py-8 lg:py-20": sideContentPadding,
            })}
          >
            {children}
          </div>
        </div>

        {/* side content */}
        {isOtherContent && (
          <div
            className={clsx(
              "h-full flex overflow-hidden",
              {
                "order-1 lg:order-2": !invert,
                "order-1 lg:order-1": invert,

                "hidden lg:flex": hideSideContentOnMobile,

                "py-8 lg:py-20": sideContentPadding,
              },
              sideContentClassName
            )}
            style={{
              backgroundColor: sideContentBackground,
            }}
          >
            {sideContent}
          </div>
        )}

        {isIllustration && (
          <div
            className={clsx(
              "h-full flex overflow-hidden items-center justify-center lg:items-end",
              {
                "order-1 lg:order-2": !invert,
                "order-1 lg:order-1": invert,

                "w-screen lg:w-full-outside-container -ml-4 lg:ml-0 lg:border-l-3":
                  !invert,
                "w-screen -ml-4 lg:-mr-[3px] lg:-ml-full-outside-container lg:w-auto lg:border-r-3":
                  invert,

                "hidden lg:flex": hideSideContentOnMobile,
              }
            )}
            style={{
              backgroundColor: sideContentBackground,
            }}
          >
            <div
              className={clsx("h-80 lg:h-128 shrink-0 flex items-end", {
                "lg:mr-auto lg:ml-4": !invert,
                "lg:ml-auto lg:mr-4": invert,
              })}
              ref={illustrationRef}
            >
              {sideContent}
            </div>
          </div>
        )}
      </Container>
    </div>
  );
};
