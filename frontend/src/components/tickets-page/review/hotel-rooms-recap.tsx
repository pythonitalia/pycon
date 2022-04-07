/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, jsx, Text } from "theme-ui";

import { Link } from "~/components/link";
import { useCurrentLanguage } from "~/locale/context";

import { HotelRoom, SelectedHotelRooms } from "../types";
import { ReviewItem } from "./review-item";

type Props = {
  selectedHotelRooms: SelectedHotelRooms;
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  };
};

export const HotelRoomsRecap: React.SFC<Props> = ({
  selectedHotelRooms,
  hotelRoomsById,
}) => {
  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    month: "long",
    day: "2-digit",
    timeZone: "Europe/Rome",
  });
  const hotelRooms = Object.values(selectedHotelRooms).flat();

  if (hotelRooms.length === 0) {
    return null;
  }

  return (
    <Box sx={{ py: 5, borderTop: "primary" }}>
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Heading
          as="h2"
          sx={{
            color: "orange",
            textTransform: "uppercase",
            mb: 4,
            fontWeight: "bold",
          }}
        >
          <FormattedMessage id="orderReview.hotelRooms" />
        </Heading>

        {hotelRooms.map((selectedRoomInfo, index) => {
          const room = hotelRoomsById[selectedRoomInfo.id];

          return (
            <Box
              key={`${selectedRoomInfo.id}-${index}`}
              sx={{
                my: 4,
              }}
            >
              <Heading
                as="h3"
                sx={{
                  textTransform: "uppercase",
                  fontSize: 3,
                  mb: 4,
                  fontWeight: "bold",
                }}
              >
                {room.name}
              </Heading>

              <Grid
                gap={3}
                sx={{
                  gridTemplateColumns: "1fr 1fr",
                  maxWidth: 400,
                }}
              >
                <ReviewItem
                  label={<FormattedMessage id="orderReview.checkin" />}
                  value={dateFormatter.format(
                    selectedRoomInfo.checkin.toDate(),
                  )}
                />
                <ReviewItem
                  label={<FormattedMessage id="orderReview.checkout" />}
                  value={dateFormatter.format(
                    selectedRoomInfo.checkout.toDate(),
                  )}
                />
              </Grid>

              <Box
                sx={{
                  maxWidth: "660px",
                  mt: 4,
                  py: 3,
                  gridColumn: "1 / 3",
                  borderTop: "primary",
                  borderBottom: "primary",
                }}
              >
                <Text
                  sx={{
                    fontSize: 4,
                    fontWeight: "bold",
                  }}
                >
                  <FormattedMessage
                    id="orderReview.hotelPrice"
                    values={{
                      roomPrice: room.price,
                      numNights: selectedRoomInfo.numNights,
                    }}
                  />
                </Text>
              </Box>
            </Box>
          );
        })}

        <Link
          variant="button"
          sx={{
            mt: 5,
            px: 4,
            py: 2,
            textTransform: "uppercase",
            backgroundColor: "cinderella",
          }}
          path={`/tickets/`}
        >
          <FormattedMessage id="orderReview.edit" />
        </Link>
      </Box>
    </Box>
  );
};
