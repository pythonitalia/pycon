import { Badge } from "@theme-ui/components";
import React from "react";

import { SubmissionTag } from "../../generated/graphql-backend";

type Props = {
  tag: SubmissionTag;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
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
