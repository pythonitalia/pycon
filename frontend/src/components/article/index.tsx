/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import { GatsbyImageProps } from "gatsby-image";
import { Fragment } from "react";
import { jsx } from "theme-ui";

type ArticleProps = {
  hero: GatsbyImageProps | null;
  title: string;
  description?: string;
};

export const Article: React.SFC<ArticleProps> = props => (
  <Fragment>
    <Heading sx={{ fontSize: 6, mb: 5 }}>{props.title}</Heading>

    <Box className="article" sx={{ mb: 5 }}>
      {props.children}
    </Box>
  </Fragment>
);
