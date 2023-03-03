import {
  Text,
  Heading,
  Link,
  Spacer,
  VerticalStack,
  Button,
  Tag,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { MyProfileWithSubmissionsQuery } from "~/types";

import { createHref } from "../link";
import { EventTag } from "../schedule-event-detail/event-tag";
import { Table } from "../table";

type Props = {
  submissions: MyProfileWithSubmissionsQuery["me"]["submissions"];
};
export const MyProposalsTable = ({ submissions }: Props) => {
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
      cols={4}
      rowGetter={(row) => {
        const inSchedule = row.scheduleItems.length > 0;
        return [
          <div>
            <EventTag type={row.type.name.toLowerCase()} />
            <Spacer size="small" />
            <Link
              href={createHref({
                path: `/submission/${row.id}`,
                locale: language,
              })}
            >
              <Heading color="none" size={4}>
                {row.title}
              </Heading>
            </Link>
          </div>,
          <StatusTag status={row.status} />,
          <div>
            {!inSchedule && (
              <Text size={2} weight="strong" as="p">
                <FormattedMessage id="profile.myProposals.notScheduled" />
              </Text>
            )}
            {inSchedule &&
              row.scheduleItems.map((scheduleItem) => {
                const parsedStartTime = parseISO(scheduleItem.start);
                const parsedEndTime = parseISO(scheduleItem.end);

                return (
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
                    <StatusTag status={scheduleItem.status} />
                  </VerticalStack>
                );
              })}
          </div>,
          <div className="flex flex-col items-start gap-2">
            {inSchedule && (
              <Button
                href={createHref({
                  path: `/schedule/invitation/${row.id}`,
                  locale: language,
                })}
                role="secondary"
                size="small"
              >
                <FormattedMessage id="profile.myProposals.viewInvitation" />
              </Button>
            )}
            <Button
              href={createHref({
                path: `/submission/${row.id}/edit`,
                locale: language,
              })}
              role="secondary"
              size="small"
            >
              <FormattedMessage id="profile.myProposals.edit" />
            </Button>
          </div>,
        ];
      }}
      keyGetter={(row) => row.id}
      data={submissions}
    />
  );
};

const StatusTag = ({
  status,
}: {
  status:
    | string
    | "waiting_confirmation"
    | "proposed"
    | "accepted"
    | "confirmed"
    | "rejected"
    | "cant_attend"
    | "cancelled"
    | "maybe";
}) => {
  switch (status) {
    case "waiting_confirmation":
      return (
        <Tag color="yellow">
          <FormattedMessage id="profile.myProposals.status.waiting" />
        </Tag>
      );
    case "confirmed":
      return (
        <Tag color="green">
          <FormattedMessage id="profile.myProposals.status.confirmed" />
        </Tag>
      );
    case "rejected":
      return (
        <Tag color="red">
          <FormattedMessage id="profile.myProposals.status.speakerRejected" />
        </Tag>
      );
    case "cant_attend":
      return (
        <Tag color="red">
          <FormattedMessage id="profile.myProposals.status.speakerCantAttend" />
        </Tag>
      );
    case "maybe":
      return (
        <Tag color="yellow">
          <FormattedMessage id="profile.myProposals.status.maybe" />
        </Tag>
      );
    case "proposed":
      return (
        <Tag color="yellow">
          <FormattedMessage id="profile.myProposals.status.proposed" />
        </Tag>
      );
    case "accepted":
      return (
        <Tag color="green">
          <FormattedMessage id="profile.myProposals.status.accepted" />
        </Tag>
      );
    case "cancelled":
      return (
        <Tag color="red">
          <FormattedMessage id="profile.myProposals.status.canceled" />
        </Tag>
      );
  }
};
