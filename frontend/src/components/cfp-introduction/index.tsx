import { Heading, Link, Spacer, Text } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { useCurrentLanguage } from "~/locale/context";

import { Fragment } from "react";
import { useIsClient } from "~/helpers/use-is-client";
import { createHref } from "../link";

export const Introduction = ({ deadline }: { deadline?: string }) => {
  const isClient = useIsClient();
  const language = useCurrentLanguage();

  return (
    <Fragment>
      <Heading size={1}>
        <FormattedMessage id="cfp.introductionHeading" />
      </Heading>

      <Spacer size="small" />

      {deadline && isClient && (
        <Text size={2} as="p">
          <FormattedMessage
            id="cfp.introductionDeadline"
            values={{
              deadline: (
                <Text size={2} as="span" weight="strong">
                  {formatDeadlineDateTime(deadline, language)}
                </Text>
              ),
            }}
          />
        </Text>
      )}

      <Spacer size="small" />

      <Link
        href={createHref({
          path: "/call-for-proposals",
          locale: language,
        })}
      >
        <Text color="none" weight="strong" decoration="underline" size={2}>
          <FormattedMessage id="global.learnMore" />
        </Text>
      </Link>
      <Spacer size="xl" />
    </Fragment>
  );
};
