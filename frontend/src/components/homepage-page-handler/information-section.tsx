import {
  Heading,
  Button,
  Text,
  Section,
  VerticalStack,
  Spacer,
} from "@python-italia/pycon-styleguide";

import { IndexPageQuery } from "~/types";

type Props = {
  conference: IndexPageQuery["conference"];
};

export const InformationSection = ({ conference }: Props) => {
  return (
    <Section spacingSize="3xl" containerSize="medium" background="yellow">
      <VerticalStack alignItems="center">
        <Heading size="display2" align="center">
          {conference.homepageCountdownSectionTitle}
        </Heading>
        <Spacer size="large" />
        <Text align="center" size={1}>
          {conference.homepageCountdownSectionText}
        </Text>
        <Spacer size="large" />
        <Button
          href={conference.homepageCountdownSectionCTALink}
          role="secondary"
        >
          {conference.homepageCountdownSectionCTAText}
        </Button>
      </VerticalStack>
    </Section>
  );
};
