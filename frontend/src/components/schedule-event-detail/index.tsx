import {
  Button,
  Grid,
  GridColumn,
  Heading,
  Section,
  Spacer,
  StyledText,
  Text,
} from "@python-italia/pycon-styleguide";
import { LiveIcon } from "@python-italia/pycon-styleguide/icons";
import { SnakeWithPopcorn } from "@python-italia/pycon-styleguide/illustrations";
import { isAfter, isBefore, parseISO } from "date-fns";
import { zonedTimeToUtc } from "date-fns-tz";
import React from "react";
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
  type: string;
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
  slidoUrl?: string;
  sidebarExtras?: React.ReactNode;
  rooms?: string[];
  youtubeVideoId?: string;
};

const isEventLive = (startTime: string, endTime: string) => {
  const now = new Date();
  const utcStart = zonedTimeToUtc(parseISO(startTime), "Europe/Rome");
  const utcEnd = zonedTimeToUtc(parseISO(endTime), "Europe/Rome");
  return isAfter(now, utcStart) && isBefore(now, utcEnd);
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
  slidoUrl,
  spacesLeft,
  sidebarExtras,
  rooms,
  youtubeVideoId,
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
  const isLive = isEventLive(startTime, endTime);

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
            {isLive && (
              <>
                <Spacer size="medium" />
                <LiveIcon />
                <Spacer size="medium" />

                {slidoUrl && (
                  <Button size="small" href={slidoUrl}>
                    <FormattedMessage id="streaming.qa" />
                  </Button>
                )}
              </>
            )}
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
              rooms={rooms}
            >
              {sidebarExtras}
            </Sidebar>
          </GridColumn>
          <GridColumn colSpan={8}>
            {eventTitle === "TBA" && (
              <video
                muted
                loop
                autoPlay
                src="/videos/nothing-to-see-here.mp4"
                style={{
                  width: "100%",
                  zIndex: 0,
                  pointerEvents: "none",
                  objectFit: "cover",
                }}
              />
            )}
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
      {youtubeVideoId && (
        <Section>
          <div className="relative max-w-[1060px] mx-auto">
            <SnakeWithPopcorn className="absolute top-0 right-14 z-10 w-[130px] -translate-y-[63%] lg:w-[180px] lg:-translate-y-[68%] hidden md:block" />
            <div className="z-20 relative">
              <iframe
                title="Recording"
                src={`https://www.youtube.com/embed/${youtubeVideoId}`}
                allowFullScreen
                className="aspect-video p-[3px] top-0 left-0 w-full bg-black"
              />
            </div>
          </div>
        </Section>
      )}
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
