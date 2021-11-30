/** @jsxRuntime classic */

/** @jsx jsx */
import moment from "moment";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Heading, jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { HotelRoom } from "~/types";

import { Button } from "../button/button";
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

export const HotelForm = ({
  hotelRooms,
  conferenceEnd,
  conferenceStart,
  addHotelRoom,
  removeHotelRoom,
  selectedHotelRooms,
}: Props) => {
  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    month: "long",
    day: "2-digit",
  });

  return (
    <Box>
      <Heading mb={3} as="h1">
        <FormattedMessage id="order.hotelRooms" />
      </Heading>
      {hotelRooms.map((room) => (
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
              category: "hotel",
              type: "HOTEL",
              quantityLeft: room.capacityLeft,
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
                <FormattedMessage
                  id="order.hotelRoomCartInfo"
                  values={{
                    roomName: <strong>{room.name}</strong>,
                    checkin: (
                      <strong>
                        {dateFormatter.format(selectedRoom.checkin.toDate())}
                      </strong>
                    ),
                    checkout: (
                      <strong>
                        {dateFormatter.format(selectedRoom.checkout.toDate())}
                      </strong>
                    ),
                  }}
                />
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
};
