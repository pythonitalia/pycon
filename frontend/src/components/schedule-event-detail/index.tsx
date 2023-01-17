import {
  Grid,
  GridColumn,
  Heading,
  Section,
  Spacer,
  Tag,
  Text,
} from "@python-italia/pycon-styleguide";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";

import { Sidebar } from "./sidebar";
import { Speaker, SpeakerSection } from "./speaker-section";

type Props = {
  id?: string;
  slug?: string;
  type: "talk" | "workshop" | "keynote" | "lightning-talks" | "panel";
  eventTitle: string;
  elevatorPitch?: string;
  abstract?: string;
  speakers: Speaker[];
  tags?: string[];
  language: string;
  audienceLevel?: string;
  startTime?: string;
  endTime?: string;
  bookable?: boolean;
  spacesLeft?: number;
};

export const ScheduleEventDetail = ({
  id,
  slug,
  type,
  eventTitle,
  speakers,
  elevatorPitch,
  abstract,
  tags,
  language,
  audienceLevel,
  startTime,
  endTime,
  bookable = false,
  spacesLeft,
}: Props) => {
  const lang = useCurrentLanguage();
  const tagColor = getTagColor(type);
  const parsedStartTime = parseISO(startTime);
  const parsedEndTime = parseISO(endTime);
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    day: "2-digit",
    month: "long",
    weekday: "long",
  });
  const hourFormatter = new Intl.DateTimeFormat(lang, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return (
    <>
      <Section illustration="snakeHead">
        <Tag color={tagColor}>
          {type === "talk" && "Talk 🎤"}
          {type === "workshop" && "Workshop 💻"}
          {type === "keynote" && "Keynote 🖌️"}
          {type === "lightning-talks" && "Lightning Talks 🏎️"}
          {type === "panel" && "Panel 👥"}
        </Tag>
        <Spacer size="2md" />
        <Heading size={1}>{eventTitle}</Heading>
        {startTime && (
          <>
            <Spacer size="2md" />
            <Heading size={3} color="grey-700">
              {dateFormatter.format(parsedStartTime)}
            </Heading>
            <Spacer size="xs" />
            <Heading size={5} color="grey-700">
              <FormattedMessage
                id="scheduleEventDetail.eventTime"
                values={{
                  start: hourFormatter.format(parsedStartTime),
                  end: hourFormatter.format(parsedEndTime),
                }}
              />
            </Heading>
          </>
        )}
      </Section>
      <Section>
        <Grid cols={12}>
          <GridColumn colSpan={4}>
            <Sidebar
              id={id}
              slug={slug}
              bookable={bookable}
              spacesLeft={spacesLeft}
              language={language}
              audienceLevel={audienceLevel}
            />
          </GridColumn>
          <GridColumn colSpan={8}>
            {elevatorPitch && (
              <>
                <Title>
                  <FormattedMessage id="scheduleEventDetail.elevatorPitch" />
                </Title>
                <Spacer size="small" />
                <Text size={1} color="grey-900">
                  {compile(elevatorPitch).tree}
                </Text>
                <Spacer size="large" />
              </>
            )}
            {abstract && (
              <>
                <Title>
                  <FormattedMessage id="scheduleEventDetail.abstract" />
                </Title>
                <Spacer size="small" />
                <Text size={2} color="grey-900">
                  {compile(abstract).tree}
                </Text>
                <Spacer size="large" />
              </>
            )}
            {tags && (
              <>
                <Title>
                  <FormattedMessage id="scheduleEventDetail.tags" />
                </Title>
                <Spacer size="small" />
                <Text size={2} weight="strong">
                  {tags.join(", ")}
                </Text>
              </>
            )}
          </GridColumn>
        </Grid>
      </Section>
      {speakers.length > 0 && (
        <Section>
          {speakers.map((speaker, index) => (
            <>
              <SpeakerSection speaker={speaker} />
              {index !== speakers.length - 1 && <Spacer size="2xl" />}
            </>
          ))}
        </Section>
      )}
    </>
  );
};

const Title = ({ children }: { children: React.ReactNode }) => (
  <Text size="label3" uppercase weight="strong">
    {children}
  </Text>
);

const getTagColor = (type: Props["type"]): Color => {
  switch (type) {
    case "talk":
      return "green";
    case "workshop":
      return "purple";
    case "keynote":
      return "yellow";
    case "lightning-talks":
      return "caramel";
    case "panel":
      return "blue";
  }
};
