import { Tag } from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";

type Props = {
  type: string;
};
export const EventTag = ({ type }: Props) => (
  <Tag color={getTagColor(type)}>
    {type === "talk" && "Talk"}
    {(type === "workshop" || type === "training") && "Workshop"}
    {type === "keynote" && "Keynote"}
    {type === "lightning-talks" && "Lightning Talks"}
    {type === "panel" && "Panel"}
    {type === "social" && "Social"}
    {type === "announcements" && "Announcements"}
    {type === "registration" && "Registration"}
    {type === "break" && "Break"}
  </Tag>
);

export const getTagColor = (type: string): Color => {
  switch (type) {
    case "talk":
      return "green";
    case "training":
    case "workshop":
      return "pink";
    case "keynote":
      return "yellow";
    case "lightning-talks":
      return "caramel";
    case "panel":
      return "blue";
    case "announcements":
    case "registration":
      return "purple";
    case "social":
      return "coral";
  }
};
