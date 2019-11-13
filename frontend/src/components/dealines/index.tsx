/** @jsx jsx */
import { Box, Grid, Heading } from "@theme-ui/components";
import { jsx } from "theme-ui";

import { FormattedMessage } from "react-intl";

import { Fragment } from "react";

type Props = {
  deadlines: {
    name: string;
    description: string;
    start: string;
    end: string;
  }[];
};

const formatDeadlineDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("default", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const Deadlines = (props: Props) => (
  <Fragment>
    {props.deadlines.map((deadline, index) => (
      <div className="element" key={index}>
        <h2 className="title">{deadline.name}</h2>
        {
          // TODO: show timezone
        }
        <dl>
          <dt>
            <FormattedMessage id="deadlines.start" />:
          </dt>
          <dd>{formatDeadlineDate(deadline.start)}</dd>
          <dt>
            <FormattedMessage id="deadlines.end" />:
          </dt>
          <dd>{formatDeadlineDate(deadline.end)}</dd>
        </dl>
      </div>
    ))}
  </Fragment>
);
