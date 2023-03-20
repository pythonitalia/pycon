import { Color } from "./types";

export const getBackgroundClasses = (background: Color) => {
  return {
    "bg-coral": background === "coral",
    "bg-caramel": background === "caramel",
    "bg-cream": background === "cream",
    "bg-yellow": background === "yellow",
    "bg-green": background === "green",
    "bg-purple": background === "purple",
    "bg-pink": background === "pink",
    "bg-blue": background === "blue",
    "bg-red": background === "red",
    "bg-success": background === "success",
    "bg-warning": background === "warning",
    "bg-neutral": background === "neutral",
    "bg-error": background === "error",
    "bg-black": background === "black",
    "bg-grey": background === "grey",
    "bg-grey-900": background === "grey-900",
    "bg-grey-700": background === "grey-700",
    "bg-grey-500": background === "grey-500",
    "bg-grey-250": background === "grey-250",
    "bg-grey-100": background === "grey-100",
    "bg-grey-50": background === "grey-50",
    "bg-white": background === "white",
    "bg-milk": background === "milk",
  };
};

export const getHoverBackgroundColor = (background?: Color | "none") => {
  return {
    "hover:bg-coral": background === "coral",
    "hover:bg-caramel": background === "caramel",
    "hover:bg-cream": background === "cream",
    "hover:bg-yellow": background === "yellow",
    "hover:bg-green": background === "green",
    "hover:bg-purple": background === "purple",
    "hover:bg-pink": background === "pink",
    "hover:bg-blue": background === "blue",
    "hover:bg-red": background === "red",
    "hover:bg-success": background === "success",
    "hover:bg-warning": background === "warning",
    "hover:bg-neutral": background === "neutral",
    "hover:bg-error": background === "error",
    "hover:bg-black": background === "black",
    "hover:bg-grey": background === "grey",
    "hover:bg-grey-900": background === "grey-900",
    "hover:bg-grey-700": background === "grey-700",
    "hover:bg-grey-500": background === "grey-500",
    "hover:bg-grey-250": background === "grey-250",
    "hover:bg-grey-100": background === "grey-100",
    "hover:bg-grey-50": background === "grey-50",
    "hover:bg-white": background === "white",
    "hover:bg-milk": background === "milk",
  };
};

export const getStyleClassesTextColor = (color: Color | "none" | "default") => {
  switch (color) {
    case "default":
    case "black":
      return "text-black";
    case "coral":
      return "text-coral";
    case "caramel":
      return "text-caramel";
    case "cream":
      return "text-cream";
    case "yellow":
      return "text-yellow";
    case "green":
      return "text-green";
    case "purple":
      return "text-purple";
    case "pink":
      return "text-pink";
    case "blue":
      return "text-blue";
    case "red":
    case "error":
      return "text-red";
    case "success":
      return "text-success";
    case "warning":
      return "text-warning";
    case "neutral":
      return "text-neutral";
    case "white":
      return "text-white";
    case "milk":
      return "text-milk";
    case "grey-900":
      return "text-grey-900";
    case "grey-700":
      return "text-grey-700";
    case "grey-500":
      return "text-grey-500";
    case "grey-250":
      return "text-grey-250";
    case "grey-100":
      return "text-grey-100";
    case "grey-50":
      return "text-grey-50";
    default:
      return "";
  }
};
