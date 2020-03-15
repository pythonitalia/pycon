import { Badge } from "@theme-ui/components";
import React from "react";

type Props = {
  tag: { name: string };
  onClick?: React.MouseEventHandler<HTMLDivElement>;
  variant?: "tag" | "selectedTag";
  className?: string;
};

export const Tag: React.SFC<Props> = ({
  tag,
  onClick,
  className,
  variant = "tag",
}) => (
  <Badge className={className} variant={variant} onClick={onClick}>
    {tag.name}
  </Badge>
);
