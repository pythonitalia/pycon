import {
  StyledText,
  Grid,
  GridColumn,
  Heading,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";

import {
  Participant,
  ParticipantInfoSection,
} from "../participant-info-section";
import { EventTag } from "./event-tag";
import { Sidebar } from "./sidebar";

type Props = {
  id?: string;
  slug?: string;
  type: "talk" | "workshop" | "keynote" | "lightning-talks" | "panel";
  eventTitle: string;
  elevatorPitch?: string;
  abstract?: string;
  speakers: Participant[];
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
        <EventTag type={type} />
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
                <StyledText baseTextSize={1}>
                  {compile(elevatorPitch).tree}
                </StyledText>
                <Spacer size="large" />
              </>
            )}
            {abstract && (
              <>
                <Title>
                  <FormattedMessage id="scheduleEventDetail.abstract" />
                </Title>
                <Spacer size="small" />
                <StyledText baseTextSize={2}>
                  {compile(abstract).tree}
                </StyledText>
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
              <ParticipantInfoSection participant={speaker} />
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
