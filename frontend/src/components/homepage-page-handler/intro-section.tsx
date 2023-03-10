import {
  Heading,
  Text,
  Section,
  Spacer,
  LayoutContent,
} from "@python-italia/pycon-styleguide";

import { IndexPageQuery } from "~/types";

type Props = {
  conference: IndexPageQuery["conference"];
};
export const IntroSection = ({ conference }: Props) => {
  return (
    <Section background="coral" spacingSize="xl" illustration="snakeLongNeck">
      <Text uppercase size={1} weight="strong">
        {conference.introPretitle}
      </Text>
      <Spacer size="xl" />

      <Heading size="display1">{conference.introTitle}</Heading>

      <LayoutContent showFrom="desktop">
        <Spacer size="xl" />
      </LayoutContent>
    </Section>
  );
};
