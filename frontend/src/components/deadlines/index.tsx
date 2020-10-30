/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/get-initial-locale";

type Props = {
  deadlines: {
    name: string;
    description: string;
    start: string;
    end: string;
  }[];
};

const formatDeadlineDate = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const Deadlines = (props: Props) => {
  const language = useCurrentLanguage();

  return (
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
            <dd>{formatDeadlineDate(deadline.start, language)}</dd>
            <dt>
              <FormattedMessage id="deadlines.end" />:
            </dt>
            <dd>{formatDeadlineDate(deadline.end, language)}</dd>
          </dl>
        </div>
      ))}
    </Fragment>
  );
};
