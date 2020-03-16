/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import {
  Alert,
  Box,
  Button,
  Flex,
  Grid,
  Heading,
  Text,
} from "@theme-ui/components";
import React, { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";
import {
  BookWorkshopMutation,
  BookWorkshopMutationVariables,
  CheckCanBookEventQuery,
  CheckCanBookEventQueryVariables,
} from "../../generated/graphql-backend";
import BOOK_WORKSHOP from "./book-workshop.graphql";
import CANCEL_WORKSHOP_BOOKING from "./cancel-workshop-booking.graphql";
import CHECK_CAN_BOOK_EVENT from "./check-can-book-event.graphql";

type Props = {
  id: string;
  slug: string;
};

export const BookWorkshop: React.SFC<Props> = ({ slug, id }) => {
  const { code } = useConference();
  const { loading, error, data: canBookEventData } = useQuery<
    CheckCanBookEventQuery,
    CheckCanBookEventQueryVariables
  >(CHECK_CAN_BOOK_EVENT, {
    variables: {
      conference: code,
      talk: slug,
    },
  });

  const [
    bookWorkshop,
    {
      loading: bookWorkshopLoading,
      error: bookWorkshopError,
      data: bookWorkshopData,
    },
  ] = useMutation<BookWorkshopMutation, BookWorkshopMutationVariables>(
    BOOK_WORKSHOP,
    {
      variables: {
        conference: code,
        id,
      },
      update(cache, { data }) {
        if (data?.bookScheduleItem.__typename === "BookScheduleItemError") {
          return;
        }

        const cachedQuery = cache.readQuery<
          CheckCanBookEventQuery,
          CheckCanBookEventQueryVariables
        >({
          query: CHECK_CAN_BOOK_EVENT,
          variables: {
            conference: code,
            talk: slug,
          },
        });

        cache.writeQuery<
          CheckCanBookEventQuery,
          CheckCanBookEventQueryVariables
        >({
          query: CHECK_CAN_BOOK_EVENT,
          variables: {
            conference: code,
            talk: slug,
          },
          data: {
            conference: {
              ...cachedQuery!.conference,
              talk: {
                ...cachedQuery!.conference.talk,
                isBooked: data!.bookScheduleItem.scheduleItem.isBooked,
                canBook: data!.bookScheduleItem.scheduleItem.canBook,
              },
            },
          },
        });
      },
    },
  );

  const [
    cancelBooking,
    {
      loading: cancelBookingLoading,
      error: cancelBookingError,
      data: cancelBookingData,
    },
  ] = useMutation(CANCEL_WORKSHOP_BOOKING, {
    variables: {
      conference: code,
      id,
    },
    update(cache, { data }) {
      if (
        data?.releaseScheduleItemBooking.__typename ===
        "ReleaseScheduleItemBookingError"
      ) {
        return;
      }

      const cachedQuery = cache.readQuery<
        CheckCanBookEventQuery,
        CheckCanBookEventQueryVariables
      >({
        query: CHECK_CAN_BOOK_EVENT,
        variables: {
          conference: code,
          talk: slug,
        },
      });

      cache.writeQuery<CheckCanBookEventQuery, CheckCanBookEventQueryVariables>(
        {
          query: CHECK_CAN_BOOK_EVENT,
          variables: {
            conference: code,
            talk: slug,
          },
          data: {
            conference: {
              ...cachedQuery!.conference,
              talk: {
                ...cachedQuery!.conference.talk,
                isBooked: data!.releaseScheduleItemBooking.scheduleItem
                  .isBooked,
                canBook: data!.releaseScheduleItemBooking.scheduleItem.canBook,
              },
            },
          },
        },
      );
    },
  });

  if (loading) {
    return null;
  }

  if (error) {
    return (
      <Alert variant="alert">
        <FormattedMessage id="talk.unableToCheckWorkshop" />
      </Alert>
    );
  }

  const talk = canBookEventData!.conference.talk!;

  return (
    <Box
      sx={{
        marginTop: [3, 3, 5, 4],
      }}
    >
      {(bookWorkshopLoading || cancelBookingLoading) && (
        <Alert sx={{ mb: 3 }} variant="info">
          <FormattedMessage id="talk.pleaseWait" />
        </Alert>
      )}

      {talk.isBooked && (
        <Fragment>
          <Text sx={{ mb: 2 }}>
            <FormattedMessage id="talk.youHaveASeat" />
          </Text>
          <Button onClick={cancelBooking}>
            <FormattedMessage id="talk.cancelBooking" />
          </Button>
        </Fragment>
      )}

      {talk.canBook && !talk.isBooked && (
        <Button onClick={bookWorkshop}>
          <FormattedMessage id="talk.bookWorkshop" />
        </Button>
      )}
    </Box>
  );
};
