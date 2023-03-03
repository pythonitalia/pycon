import clsx from "clsx";
import React, { useState, useRef, useEffect } from "react";
import { Text } from "../text";
import { Action } from "./types";
import { getIcon } from "../icons/icons";

type ActionProps = Action & {
  className?: string;
};

export const ActionItem = ({
  className,
  text,
  onClick,
  link,
  icon,
}: ActionProps) => {
  const Component = link ? "a" : "div";
  const [widths, setWidths] = useState<{
    withTextWidth: number;
    iconOnlyWidth: number;
  } | null>(null);
  const [isHovering, setIsHovering] = useState(false);
  const rootElement = useRef<any>();
  const textElement = useRef<HTMLDivElement>();

  const calculateWidths = () => {
    if (!rootElement.current) {
      return;
    }
    // get the dimensions of the action with and without text
    // this is needed to animate the width of the action
    // when hovering
    // we need to do this because we can't animate the width
    // of the action when it's set to "auto"

    // reset width to auto, in case we are re-calculating
    rootElement.current!.style.width = "auto";

    // get the width of the action without text
    const withoutText = rootElement.current!.getBoundingClientRect().width;
    textElement.current!.classList.remove("absolute");

    requestAnimationFrame(() => {
      if (!rootElement.current) {
        return;
      }

      // reducing a bit to compensate for the padding and make it look better
      const withText = rootElement.current!.getBoundingClientRect().width - 26;

      textElement.current!.classList.add("absolute");
      rootElement.current!.style.width = `${withoutText}px`;

      setWidths({
        withTextWidth: withText,
        iconOnlyWidth: withoutText,
      });
    });
  };

  useEffect(() => {
    if (!text) {
      return;
    }

    let timer: number;
    const listener = () => {
      if (timer) {
        clearTimeout(timer);
      }

      timer = window.setTimeout(calculateWidths, 100);
    };

    calculateWidths();

    window.addEventListener("resize", listener);
    return () => {
      window.removeEventListener("resize", listener);
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, []);

  const extendAction = () => {
    if (!widths) {
      return;
    }

    if (window.matchMedia("(min-width: 599px)").matches) {
      setIsHovering(true);
    }
  };

  const shrinkAction = () => {
    if (!widths) {
      return;
    }

    setIsHovering(false);
  };

  const IconComponent = getIcon(icon);

  return (
    <Component
      className={clsx(
        `bg-cream h-full p-3 lg:p-5 border-3 border-black flex items-center uppercase cursor-pointer overflow-hidden`,
        className,
        "navbar-actionitem",
        {
          "hover:bg-green": icon !== "close",
          "hover:bg-coral": icon === "close",
        }
      )}
      style={{
        width:
          (isHovering ? widths?.withTextWidth : widths?.iconOnlyWidth) ??
          "auto",
      }}
      onMouseOver={extendAction}
      onMouseOut={shrinkAction}
      onClick={onClick}
      href={link}
      ref={rootElement}
    >
      <div className="w-8 h-8">
        <IconComponent full />
      </div>

      {/* margin left of this element is basically: size of the icon (32px, w-8) + actual margin we want */}
      {/* (w-8) 32px + (ml-5) 20px = 52px */}
      {text && (
        <Text
          size={1}
          weight="strong"
          className={clsx(
            "ml-[52px] absolute navbar-actionitem-text whitespace-nowrap",
            {
              "visible opacity-100": isHovering,
              "invisible opacity-0": !isHovering,
            }
          )}
          ref={textElement}
        >
          {text}
        </Text>
      )}
    </Component>
  );
};
