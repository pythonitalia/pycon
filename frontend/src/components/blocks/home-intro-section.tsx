import {
  Heading,
  Text,
  Section,
  Spacer,
  LayoutContent,
} from "@python-italia/pycon-styleguide";

type Props = {
  pretitle: string;
  title: string;
};
export const HomeIntroSection = ({ pretitle, title }: Props) => {
  return (
    <Section background="coral" spacingSize="xl" illustration="snakeLongNeck">
      <Text uppercase size={1} weight="strong">
        {pretitle}
      </Text>
      <Spacer size="xl" />

      <Heading size="display1">{title}</Heading>

      <LayoutContent showFrom="desktop">
        <Spacer size="xl" />
      </LayoutContent>
    </Section>
  );
};
