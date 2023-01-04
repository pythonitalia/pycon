import React from "react";
import { Text } from "../text";
import clsx from "clsx";
import { TicketsIcon } from "../icons/tickets";
import { TShirtIcon } from "../icons/tshirt";
import { HotelIcon } from "../icons/hotel";
import { StarIcon } from "../icons/star";
import { ArrowDownIcon } from "../icons/arrow-down";
import { useMultiPartsCardContext } from "./context";
import { FormattedMessage } from "react-intl";

type Icon = "ticket" | "tshirt" | "hotel" | "star";
type IconBackground = "green" | "pink" | "blue" | "yellow";

type CardPartProps = React.PropsWithChildren<{
  noBg?: boolean;
  contentAlign?: "right" | "left" | "center";
  icon?: Icon;
  iconBackground?: IconBackground;
  id?: string;
  openLabel?: string | React.ReactNode;
  closeLabel?: string | React.ReactNode;
  fullHeight?: boolean;
  shrink?: boolean;
}>;

export const CardPart = ({
  children,
  noBg = false,
  contentAlign = "center",
  icon,
  iconBackground,
  id,
  openLabel,
  closeLabel,
  fullHeight = false,
  shrink = true,
}: CardPartProps) => {
  const { isClickablePart, isTargetPart, open, toggleOpen } =
    useMultiPartsCardContext();

  const isClickToExpandElement = isClickablePart(id);
  const canBeOpened = isTargetPart(id);

  const onToggleExpand = () => {
    if (isClickToExpandElement) {
      toggleOpen?.((expanded) => !expanded);
    }
  };

  const hasIcon = !!icon;

  return (
    <div
      className={clsx("overflow-hidden transition-all px-4 lg:px-6", {
        "bg-milk": noBg,
        "bg-cream": !noBg,

        "text-right": contentAlign === "right",
        "text-left": contentAlign === "left",
        "text-center": contentAlign === "center",

        "py-4 lg:py-6": !canBeOpened || open,
        "h-0 py-0 -mb-0.6": canBeOpened && !open,

        "cursor-pointer": isClickToExpandElement,

        "h-full": fullHeight,
        "shrink-0": !shrink,
      })}
      onClick={onToggleExpand}
      data-expand-own-id={id}
    >
      <div
        className={clsx("flex", {
          "flex-col": !hasIcon,
          "flex-row": hasIcon,
        })}
      >
        {icon && <Icon iconBackground={iconBackground} icon={icon} />}
        <div
          className={clsx({
            "pl-4 ml-4 lg:ml-6 lg:pl-6": !!icon,
            "flex justify-between items-center w-full": isClickToExpandElement,
          })}
        >
          {children}

          {isClickToExpandElement && (
            <div className="flex items-center justify-center gap-4 select-none">
              {!open && (
                <Text className="hidden md:block" uppercase size="label3">
                  {openLabel || (
                    <FormattedMessage
                      defaultMessage="Open"
                      id="multiple-parts-card.openLabel"
                    />
                  )}
                </Text>
              )}

              {open && (
                <Text className="hidden md:block" uppercase size="label3">
                  {closeLabel || (
                    <FormattedMessage
                      defaultMessage="Close"
                      id="multiple-parts-card.closeLabel"
                    />
                  )}
                </Text>
              )}

              <ArrowDownIcon
                className={clsx("transition-transform", {
                  "rotate-0": !open,
                  "rotate-180": open,
                })}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Icon = ({
  icon,
  iconBackground,
}: {
  icon: CardPartProps["icon"];
  iconBackground: CardPartProps["iconBackground"];
}) => {
  let Component;
  switch (icon) {
    case "ticket":
      Component = TicketsIcon;
      break;
    case "tshirt":
      Component = TShirtIcon;
      break;
    case "hotel":
      Component = HotelIcon;
      break;
    case "star":
      Component = StarIcon;
      break;
  }

  return (
    <div
      className={clsx(
        "inline-flex items-center justify-center p-4 -m-4 lg:p-6 lg:-m-6 border-r",
        {
          "bg-green": iconBackground === "green",
          "bg-pink": iconBackground === "pink",
          "bg-blue": iconBackground === "blue",
          "bg-yellow": iconBackground === "yellow",
        }
      )}
    >
      <div className="w-8 h-8 lg:w-12 lg:h-12">
        <Component className="w-full h-full" />
      </div>
    </div>
  );
};
