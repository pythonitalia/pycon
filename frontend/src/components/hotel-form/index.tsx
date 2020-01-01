/** @jsx jsx */
import { Box, Button, Flex, Heading } from "@theme-ui/components";
import moment from "moment";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { HotelRoom } from "../../generated/graphql-backend";
import { DATE_FORMAT } from "../tickets-form/add-hotel-room";
import { ProductRow } from "../tickets-form/product-row";
import { SelectedHotelRooms } from "../tickets-page/types";

type Props = {
  hotelRooms: HotelRoom[];
  conferenceStart: string;
  conferenceEnd: string;
  selectedHotelRooms: SelectedHotelRooms;
  addHotelRoom: (
    id: string,
    checkin: moment.Moment,
    checkout: moment.Moment,
  ) => void;
  removeHotelRoom: (id: string, index: number) => void;
};

export const HotelForm: React.SFC<Props> = ({
  hotelRooms,
  conferenceEnd,
  conferenceStart,
  addHotelRoom,
  removeHotelRoom,
  selectedHotelRooms,
}) => (
  <Box>
    <Heading mb={3} as="h2">
      Hotel rooms
    </Heading>
    {hotelRooms.map(room => (
      <Box
        sx={{
          mb: 4,
        }}
        key={room.id}
      >
        <ProductRow
          sx={{
            marginBottom: 0,
          }}
          hotel={true}
          conferenceStart={conferenceStart}
          conferenceEnd={conferenceEnd}
          addHotelRoom={addHotelRoom}
          ticket={{
            ...room,
            soldOut:
              room.isSoldOut ||
              (selectedHotelRooms[room.id] ?? []).length >= room.capacityLeft,
            defaultPrice: room.price,
            questions: [],
          }}
        />
        {(selectedHotelRooms[room.id] ?? []).map((selectedRoom, index) => (
          <Flex
            key={index}
            sx={{
              justifyContent: "space-between",
              alignItems: "center",

              mt: 2,
            }}
          >
            <Box>
              <strong>{room.name}</strong>{" "}
              <FormattedMessage id="order.withChekinThe" />{" "}
              <strong>{selectedRoom.checkin.format(DATE_FORMAT)}</strong>{" "}
              <FormattedMessage id="order.withChekoutThe" />{" "}
              <strong>{selectedRoom.checkout.format(DATE_FORMAT)}</strong>
            </Box>
            <Button
              sx={{
                marginLeft: 4,
                flexShrink: 0,
              }}
              variant="minus"
              onClick={() => removeHotelRoom(room.id, index)}
            >
              -
            </Button>
          </Flex>
        ))}
      </Box>
    ))}
  </Box>
);
