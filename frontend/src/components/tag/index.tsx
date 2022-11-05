/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { Badge, jsx } from "theme-ui";

type Props = {
  tag: { name: string };
  onClick?: React.MouseEventHandler<HTMLDivElement>;
  variant?: "tag" | "selectedTag";
  className?: string;
};

export const Tag = ({ tag, onClick, className, variant = "tag" }: Props) => (
  <Badge className={className} variant={variant} onClick={onClick}>
    {tag.name}
  </Badge>
);
