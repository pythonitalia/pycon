/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { Fragment } from "react";
import { jsx } from "theme-ui";

type ArticleProps = {
  title: string;
  published?: string;
  description?: string;
};

const formateDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("default", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const Article: React.SFC<ArticleProps> = (props) => (
  <Fragment>
    <Heading sx={{ fontSize: 6 }}>{props.title}</Heading>
    {props.published && (
      <Text sx={{ fontSize: 2, mt: 3, fontWeight: "bold", color: "orange" }}>
        {formateDate(props.published)}
      </Text>
    )}

    <Box sx={{ mt: 4, mb: 5 }} className="article">
      {props.children}
    </Box>
  </Fragment>
);
