import { GatsbyImageProps } from "gatsby-image";
import React from "react";

type ArticleProps = {
  hero: GatsbyImageProps | null;
  title: string;
  description?: string;
};

export const Article: React.SFC<ArticleProps> = props => (
  <div className="content">{props.children}</div>
);
