import {
  Heading,
  Link,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";

export const Introduction = ({ deadline }: { deadline?: string }) => {
  const language = useCurrentLanguage();
  return (
    <Section illustration="snakeHead">
      <Heading size={1}>
        <FormattedMessage id="cfp.introductionHeading" />
      </Heading>
      <Spacer size="thin" />

      <Heading size={3}>
        <FormattedMessage id="cfp.introductionSubtitle" />
      </Heading>
      <Spacer size="small" />
      <Text size={2} as="p">
        <FormattedMessage id="cfp.introductionCopy" />
      </Text>

      {deadline && (
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
      <Spacer size="medium" />
      <Link
        href={createHref({
          path: "/call-for-proposals",
          locale: language,
        })}
      >
        <Text weight="strong" decoration="underline">
          <FormattedMessage id="global.learnMore" />
        </Text>
      </Link>
    </Section>
  );
};
