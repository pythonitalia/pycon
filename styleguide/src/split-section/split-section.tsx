import clsx from "clsx";
import React, { useEffect, useRef } from "react";
import { Heading } from "../heading";
import { Separator } from "../separator";
import { Container } from "../container";
import { Spacer } from "../spacer/spacer";

type Props = {
  children: React.ReactNode;
  title: string | React.ReactNode;
  sideContent: React.ReactNode;
  sideContentBackground?: string;
  sideContentType?: "illustration" | "other";
  invert?: boolean;
  hideSideContentOnMobile?: boolean;
  spacing?: "even" | "larger-content";
};

export const SplitSection = ({
  title,
  children,
  sideContent,
  sideContentBackground,
  sideContentType = "illustration",
  spacing = "even",
  hideSideContentOnMobile = false,
  invert = false,
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
        className={clsx("grid", {
          "grid-cols-1 lg:grid-cols-2": spacing === "even",
          "grid-cols-1 lg:gap-24": spacing === "larger-content",
          "lg:grid-cols-split-content-larger-content":
            spacing === "larger-content" && !invert,
          "lg:grid-cols-inverted-split-content-larger-content":
            spacing === "larger-content" && invert,
        })}
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
            className={clsx(
              "h-full py-8 lg:py-20 flex justify-center items-start flex-col",
              {
                "lg:pr-10": !invert,
                "lg:pl-10": invert,
              }
            )}
          >
            <Heading size="display2">{title}</Heading>
            <Spacer size="medium" />
            {children}
          </div>
        </div>

        {/* side content */}
        {isOtherContent && (
          <div
            className={clsx("h-full flex overflow-hidden py-8 lg:py-20", {
              "order-1 lg:order-2": !invert,
              "order-1 lg:order-1": invert,

              "hidden lg:flex": hideSideContentOnMobile,
            })}
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
