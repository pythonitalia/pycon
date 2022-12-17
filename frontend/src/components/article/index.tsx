/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { Box, Heading, jsx, Text } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";

type ArticleProps = {
  title?: string;
  published?: string;
  description?: string;
  className?: string;
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

export const Article = (props: React.PropsWithChildren<ArticleProps>) => {
  const language = useCurrentLanguage();

  return (
    <Fragment>
      {props.title && <Heading sx={{ fontSize: 6 }}>{props.title}</Heading>}
      {props.published && (
        <Text sx={{ fontSize: 2, mt: 3, fontWeight: "bold", color: "orange" }}>
          {formateDate(props.published, language)}
        </Text>
      )}

      <Box sx={{ mt: 4 }} className={`article ${props.className}`}>
        {props.children}
      </Box>
    </Fragment>
  );
};
