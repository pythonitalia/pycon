import {
  Spacer,
  Text,
  CardPart,
  MultiplePartsCard,
  Button,
  VerticalStack,
  Link,
  Tag,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import {
  useBookScheduleItemMutation,
  useCancelBookingScheduleItemMutation,
  useWorkshopBookingStateQuery,
} from "~/types";

import { ErrorsList } from "../errors-list";
import { createHref } from "../link";
import { useLoginState } from "../profile/hooks";

type Props = {
  id: string;
  slug: string;
  language: string;
  audienceLevel?: string;
  bookable: boolean;
  spacesLeft?: number;
  children?: React.ReactNode;
  rooms?: string[];
};

export const Sidebar = ({
  id,
  slug,
  spacesLeft,
  bookable,
  language,
  audienceLevel,
  children,
  rooms,
}: Props) => {
  const lang = useCurrentLanguage();
  const [isLoggedIn] = useLoginState();
  const { data: bookingStateData, loading: isLoadingBookingState } =
    useWorkshopBookingStateQuery({
      variables: {
        code: process.env.conferenceCode,
        slug,
      },
      skip: !isLoggedIn || !bookable,
      fetchPolicy: "network-only",
      nextFetchPolicy: "cache-first",
    });

  const [
    executeBookScheduleItem,
    { data: bookSpotData, loading: isBookingSpot },
  ] = useBookScheduleItemMutation();

  const [executeCancelBooking, { loading: isCancellingBooking }] =
    useCancelBookingScheduleItemMutation();

  const bookScheduleItem = () => {
    executeBookScheduleItem({
      variables: {
        id,
      },
    });
  };

  const cancelBooking = () => {
    executeCancelBooking({
      variables: {
        id,
      },
    });
  };

  const userHasSpot = bookingStateData?.conference?.talk?.userHasSpot;

  return (
    <>
      <MultiplePartsCard>
        {rooms && (
          <EventInfo
            label={
              <FormattedMessage
                id="eventDetail.rooms"
                values={{
                  countRooms: rooms.length,
                }}
              />
            }
          >
            {rooms.join(", ")}
          </EventInfo>
        )}
        <EventInfo label={<FormattedMessage id="talk.language" />}>
          <FormattedMessage id={`talk.language.${language}`} />
        </EventInfo>
        {audienceLevel && (
          <EventInfo label={<FormattedMessage id="talk.audienceLevel" />}>
            {audienceLevel}
          </EventInfo>
        )}
        {bookable && (
          <EventInfo
            label={
              <FormattedMessage id="scheduleEventDetail.sidebar.spacesLeft" />
            }
          >
            {spacesLeft > 0 && spacesLeft}
            {spacesLeft <= 0 && (
              <Tag color="red">
                <FormattedMessage id="scheduleEvent.soldout" />
              </Tag>
            )}
          </EventInfo>
        )}
        {userHasSpot && (
          <EventInfo>
            <FormattedMessage id="talk.spotReserved" />
          </EventInfo>
        )}
      </MultiplePartsCard>
      <Spacer size="medium" />
      {bookable && (
        <VerticalStack alignItems="start">
          <ErrorsList
            errors={[
              bookSpotData?.bookScheduleItem?.__typename ===
                "ScheduleItemIsFull" && (
                <FormattedMessage id="talk.eventIsFull" />
              ),
              bookSpotData?.bookScheduleItem?.__typename ===
                "UserNeedsConferenceTicket" && (
                <FormattedMessage
                  id="talk.buyATicket"
                  values={{
                    link: (
                      <Link
                        href={createHref({
                          path: "/tickets",
                          locale: lang,
                        })}
                      >
                        <FormattedMessage id="talk.buyATicketCTA" />
                      </Link>
                    ),
                  }}
                />
              ),
            ]}
          />
          {!isLoadingBookingState &&
            isLoggedIn &&
            (spacesLeft > 0 || userHasSpot) && (
              <Button
                onClick={userHasSpot ? cancelBooking : bookScheduleItem}
                disabled={isBookingSpot || isCancellingBooking}
                size="small"
                role="secondary"
              >
                {userHasSpot && <FormattedMessage id="talk.unregisterCta" />}
                {!userHasSpot && <FormattedMessage id="talk.bookCta" />}
              </Button>
            )}
        </VerticalStack>
      )}
      {children}
    </>
  );
};

const EventInfo = ({
  label,
  children,
}: {
  children: React.ReactNode;
  label?: React.ReactNode;
}) => (
  <CardPart contentAlign="left" background="milk">
    {label && (
      <>
        <Text uppercase size="label3" weight="strong">
          {label}
        </Text>
        <Spacer size="xs" />
      </>
    )}
    <Text size="label2" weight="strong">
      {children}
    </Text>
  </CardPart>
);
