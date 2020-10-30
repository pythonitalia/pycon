/** @jsx jsx */
import { Fragment } from "react";
import { Box, Heading, jsx, Text } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/get-initial-locale";

type ArticleProps = {
  title: string;
  published?: string;
  description?: string;
};

const formateDate = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const Article: React.FC<ArticleProps> = (props) => {
  const language = useCurrentLanguage();

  return (
    <Fragment>
      <Heading sx={{ fontSize: 6 }}>{props.title}</Heading>
      {props.published && (
        <Text sx={{ fontSize: 2, mt: 3, fontWeight: "bold", color: "orange" }}>
          {formateDate(props.published, language)}
        </Text>
      )}

      <Box sx={{ mt: 4, mb: 5 }} className="article">
        {props.children}
      </Box>
    </Fragment>
  );
};
