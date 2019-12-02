import { Badge } from "@theme-ui/components";
import React from "react";

import { SubmissionTag } from "../../generated/graphql-backend";

type Props = {
  tag: SubmissionTag;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  variant?: "tag" | "selectedTag";
};

export const Tag: React.SFC<Props> = ({ tag, onClick, variant = "tag" }) => (
  <Badge variant={variant} onClick={onClick}>
    {tag.name}
  </Badge>
);
