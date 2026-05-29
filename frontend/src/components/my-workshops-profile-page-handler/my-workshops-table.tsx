import {
  Button,
  Heading,
  Link,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import type { MyProfileWithBookedWorkshopsQuery } from "~/types";

import { createHref } from "../link";
import { EventTag } from "../schedule-event-detail/event-tag";
import { Table } from "../table";

type Props = {
  workshops: MyProfileWithBookedWorkshopsQuery["me"]["bookedScheduleItems"];
};

export const MyWorkshopsTable = ({ workshops }: Props) => {
  const language = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "2-digit",
    month: "long",
    weekday: "long",
  });
  const hourFormatter = new Intl.DateTimeFormat(language, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return (
    <Table
      cols={3}
      rowGetter={(workshop) => {
        const parsedStartTime = parseISO(workshop.start);
        const parsedEndTime = parseISO(workshop.end);
        const roomNames = workshop.rooms.map((room) => room.name).join(", ");

        return [
          <div>
            <EventTag type={workshop.type.toLowerCase()} />
            <Spacer size="small" />
            <Link
              href={createHref({
                path: `/event/${workshop.slug}`,
                locale: language,
              })}
            >
              <Heading color="none" size={4}>
                {workshop.title}
              </Heading>
            </Link>
          </div>,
          <VerticalStack gap="small" alignItems="start">
            <Text size={2} weight="strong" as="p">
              <FormattedMessage
                id="profile.myProposals.date"
                values={{
                  day: dateFormatter.format(parsedStartTime),
                  start: hourFormatter.format(parsedStartTime),
                  end: hourFormatter.format(parsedEndTime),
                }}
              />
            </Text>
            {roomNames && (
              <Text size={2} as="p">
                <FormattedMessage
                  id="profile.myWorkshops.room"
                  values={{ room: roomNames }}
                />
              </Text>
            )}
          </VerticalStack>,
          <Button
            href={createHref({
              path: `/event/${workshop.slug}`,
              locale: language,
            })}
            size="small"
            variant="secondary"
          >
            <FormattedMessage id="profile.myWorkshops.viewWorkshop" />
          </Button>,
        ];
      }}
      keyGetter={(workshop) => workshop.id}
      data={workshops}
    />
  );
};
