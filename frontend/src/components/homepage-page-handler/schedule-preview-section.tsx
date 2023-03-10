import {
  BasicButton,
  Button,
  CardPart,
  Container,
  DaysSelector,
  Heading,
  Link,
  MultiplePartsCard,
  Section,
  SliderGrid,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { useState } from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { IndexPageQuery } from "~/types";

import { createHref } from "../link";

type Props = {
  days: IndexPageQuery["conference"]["days"];
};
export const SchedulePreviewSection = ({ days }: Props) => {
  const [selectedDay, setSelectedDay] = useState(days[1]);
  const language = useCurrentLanguage();

  return (
    <Section noContainer>
      <Container>
        <Heading align="center" size="display2">
          Schedule
        </Heading>
      </Container>
      <Spacer size="2xl" />

      <DaysSelector
        center={true}
        days={days.map((day) => ({
          date: day.day,
          selected: day.day === selectedDay.day,
        }))}
        language={language}
        onClick={(day) => {
          setSelectedDay(days.find((d) => d.day === day));
        }}
      />
      <Spacer size="xl" />
      <SliderGrid mdCols={2} cols={4}>
        {selectedDay.randomEvents.map((event) => (
          <ScheduleEventPreviewCard key={event.id} event={event} />
        ))}
      </SliderGrid>
      <Spacer size="xl" />
      <Container>
        <div className="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-12">
          <Button
            role="secondary"
            href={createHref({
              path: "/tickets",
              locale: language,
            })}
          >
            <FormattedMessage id="tickets.buyTickets" />
          </Button>
          <BasicButton
            href={createHref({
              path: "/schedule",
              locale: language,
            })}
          >
            <FormattedMessage id="homepage.schedulePreviewSection.goToSchedule" />
          </BasicButton>
        </div>
      </Container>
    </Section>
  );
};

const ScheduleEventPreviewCard = ({
  event,
}: {
  event: IndexPageQuery["conference"]["days"][number]["randomEvents"][number];
}) => {
  const language = useCurrentLanguage();
  const audienceLevel =
    event.audienceLevel?.name ?? event.submission?.audienceLevel?.name;
  const photo = event.speakers.find((speaker) => !!speaker.participant?.photo)
    ?.participant?.photo;
  const hourFormatter = new Intl.DateTimeFormat(language, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return (
    <div className="h-full flex flex-col">
      <div>
        <Text as="p" size="label3" weight="strong">
          <FormattedMessage
            id="homepage.eventPreviewCard.time"
            values={{
              start: hourFormatter.format(parseISO(event.start)),
              end: hourFormatter.format(parseISO(event.end)),
            }}
          />
        </Text>
        <Spacer size="xs" />
        <Text as="p" size="label4" color="grey-700">
          {[event.language?.name, audienceLevel]
            .filter((text) => text)
            .join(", ")}
        </Text>
      </div>
      <Spacer size="small" />
      <MultiplePartsCard>
        <CardPart
          shrink={false}
          contentAlign="left"
          background="milk"
          size="none"
        >
          <div className="flex divide-x">
            {photo && (
              <img
                src={photo}
                alt="Speaker photo"
                loading="lazy"
                className="w-20 aspect-square object-cover"
              />
            )}
            <Heading className="flex p-5 items-center justify-center" size={6}>
              {event.speakers.map((speaker) => speaker.fullName).join(", ")}
            </Heading>
          </div>
        </CardPart>
        <CardPart fullHeight contentAlign="left" background="cream">
          <Link
            href={createHref({
              path: `/event/${event.slug}`,
              locale: language,
            })}
          >
            <Heading color="none" size={4}>
              {event.title}
            </Heading>
          </Link>
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};
