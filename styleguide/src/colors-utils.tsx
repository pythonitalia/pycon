import { Color } from "./types";

export const getBackgroundClasses = (background: Color) => {
  switch (background) {
    case "coral":
      return "bg-coral";
    case "caramel":
      return "bg-caramel";
    case "cream":
      return "bg-cream";
    case "yellow":
      return "bg-yellow";
    case "green":
      return "bg-green";
    case "purple":
      return "bg-purple";
    case "pink":
      return "bg-pink";
    case "blue":
      return "bg-blue";
    case "red":
      return "bg-red";
    case "success":
      return "bg-success";
    case "warning":
      return "bg-warning";
    case "neutral":
      return "bg-neutral";
    case "error":
      return "bg-error";
    case "black":
      return "bg-black";
    case "grey":
      return "bg-grey";
    case "grey-900":
      return "bg-grey-900";
    case "grey-700":
      return "bg-grey-700";
    case "grey-500":
      return "bg-grey-500";
    case "grey-250":
      return "bg-grey-250";
    case "grey-100":
      return "bg-grey-100";
    case "grey-50":
      return "bg-grey-50";
    case "white":
      return "bg-white";
    case "milk":
      return "bg-milk";
    default:
      return ""
  }
};

export const getHoverBackgroundColor = (background?: Color | "none") => {
  switch (background) {
    case "coral":
      return "hover:bg-coral";
    case "caramel":
      return "hover:bg-caramel";
    case "cream":
      return "hover:bg-cream";
    case "yellow":
      return "hover:bg-yellow";
    case "green":
      return "hover:bg-green";
    case "purple":
      return "hover:bg-purple";
    case "pink":
      return "hover:bg-pink";
    case "blue":
      return "hover:bg-blue";
    case "red":
      return "hover:bg-red";
    case "success":
      return "hover:bg-success";
    case "warning":
      return "hover:bg-warning";
    case "neutral":
      return "hover:bg-neutral";
    case "error":
      return "hover:bg-error";
    case "black":
      return "hover:bg-black";
    case "grey":
      return "hover:bg-grey";
    case "grey-900":
      return "hover:bg-grey-900";
    case "grey-700":
      return "hover:bg-grey-700";
    case "grey-500":
      return "hover:bg-grey-500";
    case "grey-250":
      return "hover:bg-grey-250";
    case "grey-100":
      return "hover:bg-grey-100";
    case "grey-50":
      return "hover:bg-grey-50";
    case "white":
      return "hover:bg-white";
    case "milk":
      return "hover:bg-milk";
    default:
      return "";
  }
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
export const getStyleClassesHoverTextColor = (
  color: Color | "none" | "default"
) => {
  switch (color) {
    case "default":
    case "black":
      return "hover:text-black";
    case "coral":
      return "hover:text-coral";
    case "caramel":
      return "hover:text-caramel";
    case "cream":
      return "hover:text-cream";
    case "yellow":
      return "hover:text-yellow";
    case "green":
      return "hover:text-green";
    case "purple":
      return "hover:text-purple";
    case "pink":
      return "hover:text-pink";
    case "blue":
      return "hover:text-blue";
    case "red":
    case "error":
      return "hover:text-red";
    case "success":
      return "hover:text-success";
    case "warning":
      return "hover:text-warning";
    case "neutral":
      return "hover:text-neutral";
    case "white":
      return "hover:text-white";
    case "milk":
      return "hover:text-milk";
    case "grey-900":
      return "hover:text-grey-900";
    case "grey-700":
      return "hover:text-grey-700";
    case "grey-500":
      return "hover:text-grey-500";
    case "grey-250":
      return "hover:text-grey-250";
    case "grey-100":
      return "hover:text-grey-100";
    case "grey-50":
      return "hover:text-grey-50";
    default:
      return "";
  }
};
