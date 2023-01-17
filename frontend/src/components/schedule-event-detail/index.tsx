import {
  CardPart,
  Grid,
  GridColumn,
  Heading,
  MultiplePartsCard,
  Section,
  Spacer,
  Tag,
  Text,
} from "@python-italia/pycon-styleguide";

export type Props = {
  type: "talk" | "workshop";
  eventTitle: string;
};

export const ScheduleEventDetail = ({ type, eventTitle }: Props) => {
  return (
    <>
      <Section illustration="snakeHead">
        <Tag color="purple">
          {type === "talk" && "Talk"}
          {type === "workshop" && "Workshop"}
        </Tag>
        <Spacer size="2md" />
        <Heading size={1}>{eventTitle}</Heading>
      </Section>
      <Section>
        <Grid cols={12}>
          <GridColumn colSpan={4}>
            <MultiplePartsCard>
              <CardPart contentAlign="left" background="milk">
                <Text uppercase size="label3" weight="strong">
                  Talk Length
                </Text>
                <Spacer size="xs" />
                <Text size="label2" weight="strong">
                  30 minutes
                </Text>
              </CardPart>
              <CardPart contentAlign="left" background="milk">
                <Text uppercase size="label3" weight="strong">
                  Language
                </Text>
                <Spacer size="xs" />
                <Text size="label2" weight="strong">
                  English
                </Text>
              </CardPart>
            </MultiplePartsCard>
          </GridColumn>
          <GridColumn colSpan={8}>right</GridColumn>
        </Grid>
      </Section>
    </>
  );
};
