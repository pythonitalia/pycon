import { Heading, Spacer } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";

type ArticleProps = {
  title?: string;
};

export const Article = (props: React.PropsWithChildren<ArticleProps>) => {
  return (
    <Fragment>
      {props.title && <Heading size={1}>{props.title}</Heading>}
      <Spacer size="medium" />
      <div className="article">{props.children}</div>
    </Fragment>
  );
};
