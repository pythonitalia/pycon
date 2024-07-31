import {
  CardPart,
  CardPartOptions,
  CardPartTwoSides,
  Heading,
  MultiplePartsCard,
  Spacer,
  Tag,
  TagsCollection,
  Text,
} from "@python-italia/pycon-styleguide";
import { differenceInCalendarDays, format, isAfter, parseISO } from "date-fns";
import { useState } from "react";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import type { HotelRoom } from "~/types";

import type { HotelRoomState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

type Props = {
  hotelRoom: HotelRoom;
  openByDefault: boolean;
};

type TemporaryHotelRoomState = {
  checkin?: string;
  checkout?: string;
  beds?: string;
};

export const HotelRow = ({ hotelRoom, openByDefault }: Props) => {
  const {
    addHotelRoom,
    removeHotelRoom,
    state: { selectedHotelRooms },
  } = useCart();
  const bedLayouts = hotelRoom.availableBedLayouts;

  const [temporaryState, setTemporaryState] = useState<TemporaryHotelRoomState>(
    {},
  );

  const onChange = (id, e) => {
    setTemporaryState((temporaryRoom) => {
      const newTemporaryRoom = {
        ...temporaryRoom,
        [id]: e.target.value,
      };

      if (id === "checkin") {
        newTemporaryRoom.checkout = "";
      }

      return newTemporaryRoom;
    });
  };

  const onConfirm = () => {
    const beds =
      bedLayouts.length === 1 ? bedLayouts[0].id : temporaryState.beds;

    if (!temporaryState.checkin || !temporaryState.checkout || !beds) {
      return;
    }

    addHotelRoom(
      hotelRoom.id,
      temporaryState.checkin,
      temporaryState.checkout,
      beds,
    );
    setTemporaryState({});
  };

  const price = Number(hotelRoom.price);

  return (
    <MultiplePartsCard
      openByDefault={openByDefault}
      clickablePart={hotelRoom.description ? "heading" : undefined}
      expandTarget={hotelRoom.description ? "content" : undefined}
    >
      <CardPart
        iconBackground="green"
        icon="hotel"
        contentAlign="left"
        id="heading"
        openLabel={
          <FormattedMessage id="tickets.productsList.openDescription" />
        }
      >
        <Heading size={2}>{hotelRoom.name}</Heading>
      </CardPart>
      {hotelRoom.description && (
        <CardPart id="content" contentAlign="left" background="milk">
          <TagsCollection>
            {hotelRoom.capacityLeft > 0 ? (
              <Tag color="yellow">
                <FormattedMessage
                  id="order.ticketsLeft"
                  values={{
                    count: hotelRoom.capacityLeft,
                  }}
                />
              </Tag>
            ) : null}
          </TagsCollection>
          {hotelRoom.capacityLeft > 0 && <Spacer size="xs" />}
          <Text size={2}>{hotelRoom.description}</Text>
        </CardPart>
      )}

      {selectedHotelRooms[hotelRoom.id]?.map((selectedRoom, index) => (
        <AddViewHotelRoomRow
          key={`${selectedRoom.id}${index}`}
          onRemove={() => {
            removeHotelRoom(hotelRoom.id, index);
          }}
          action="remove"
          price={price}
          hotelRoom={selectedRoom}
          onConfirm={onConfirm}
          roomProduct={hotelRoom}
        />
      ))}

      <AddViewHotelRoomRow
        price={price}
        action="add"
        hotelRoom={temporaryState}
        onConfirm={onConfirm}
        onChange={onChange}
        roomProduct={hotelRoom}
        soldOut={hotelRoom.isSoldOut}
      />
    </MultiplePartsCard>
  );
};

const AddViewHotelRoomRow = ({
  hotelRoom,
  onConfirm,
  onChange,
  onRemove,
  price,
  action,
  roomProduct,
  soldOut,
}: {
  hotelRoom: TemporaryHotelRoomState | HotelRoomState;
  onConfirm?: () => void;
  onChange?: (id: string, e: any) => void;
  onRemove?: () => void;
  price: number;
  action: "add" | "remove";
  roomProduct: HotelRoom;
  soldOut?: boolean;
}) => {
  const bedLayouts = roomProduct.availableBedLayouts;
  const hotelCheckinParsed = parseISO(hotelRoom.checkin);
  const hotelCheckoutParsed = parseISO(hotelRoom.checkout);

  const parsedCheckInDates = roomProduct.checkInDates.map((date) =>
    parseISO(date),
  );
  const parsedCheckOutDates = roomProduct.checkOutDates
    .map((date) => parseISO(date))
    .filter((date) => isAfter(date, hotelCheckinParsed));

  const nightsBetween =
    differenceInCalendarDays(hotelCheckoutParsed, hotelCheckinParsed) || 0;

  const moneyFormatter = useMoneyFormatter();

  const leftSide = (
    <div className="h-full flex items-center lg:items-end gap-2">
      <Heading size={2}>
        <FormattedMessage
          id="tickets.hotelRow.totalPrice"
          values={{
            value: moneyFormatter.format(
              nightsBetween ? nightsBetween * price : price,
            ),
          }}
        />
      </Heading>
      <Text uppercase size="label3" weight="strong">
        <FormattedMessage
          id="tickets.hotelRow.pricePerNight"
          values={{
            nights: nightsBetween,
            price: moneyFormatter.format(price),
          }}
        />
      </Text>
    </div>
  );

  if (soldOut) {
    return (
      <CardPartTwoSides
        rightSide={
          <div className="w-full flex md:items-center md:justify-center">
            <Tag color="red">
              <FormattedMessage id="tickets.productsList.soldOut" />
            </Tag>
          </div>
        }
      >
        {leftSide}
      </CardPartTwoSides>
    );
  }

  const options = [
    {
      id: "checkin",
      options: parsedCheckInDates.map((date) => ({
        label: format(date, "dd MMMM"),
        value: format(date, "yyyy-MM-dd"),
      })),
      placeholder: (
        <FormattedMessage id="tickets.productsList.hotelRow.checkin" />
      ),
      value: hotelRoom.checkin,
    },
    {
      id: "checkout",
      options: parsedCheckOutDates.map((date) => ({
        label: format(date, "dd MMMM"),
        value: format(date, "yyyy-MM-dd"),
      })),
      placeholder: (
        <FormattedMessage id="tickets.productsList.hotelRow.checkout" />
      ),
      value: hotelRoom.checkout,
    },
  ];

  if (bedLayouts.length > 1) {
    options.push({
      id: "beds",
      options: bedLayouts.map((bedLayout) => ({
        label: bedLayout.name,
        value: bedLayout.id,
      })),
      placeholder: (
        <FormattedMessage id="tickets.productsList.hotelRow.bedLayout" />
      ),
      value: hotelRoom.beds,
    });
  }

  return (
    <CardPartOptions
      onConfirm={onConfirm}
      onChange={onChange}
      onRemove={onRemove}
      action={action}
      options={options}
    >
      {leftSide}
    </CardPartOptions>
  );
};
