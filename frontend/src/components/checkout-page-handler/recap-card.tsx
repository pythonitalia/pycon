import {
  Text,
  CardPart,
  MultiplePartsCard,
  Heading,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { HotelRoom, TicketItem } from "~/types";

import { calculateProductPrice } from "../tickets-page/review/prices";
import { HotelRoomState, ProductState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

type Props = {
  productsById: { [id: number]: TicketItem };
  hotelRoomsById: { [id: number]: HotelRoom };
};
export const RecapCard = ({ productsById, hotelRoomsById }: Props) => {
  const {
    state: { selectedHotelRooms, selectedProducts },
  } = useCart();

  return (
    <div>
      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart contentAlign="left" id="heading">
          <Heading size={2}>
            <FormattedMessage id="tickets.checkout.recap" />
          </Heading>
        </CardPart>
        <CardPart noBg contentAlign="left" id="content">
          {Object.values(selectedProducts)
            .flatMap((nestedProducts) => nestedProducts.flat())
            .map((selectedProduct, index) => {
              const product = productsById[selectedProduct.id];
              return (
                <RecapItem
                  key={`${selectedProduct.id}-${index}`}
                  product={product}
                  selectedProductInfo={selectedProduct}
                />
              );
            })}
          {Object.values(selectedHotelRooms)
            .flatMap((nestedProducts) => nestedProducts.flat())
            .map((selectedHotelRoom, index) => {
              return (
                <RecapHotelItem
                  hotelRoom={hotelRoomsById[selectedHotelRoom.id]}
                  selectedHotelRoomInfo={selectedHotelRoom}
                  key={`${selectedHotelRoom.id}-${index}`}
                />
              );
            })}
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

type RecapHotelItemProps = {
  selectedHotelRoomInfo: HotelRoomState;
  hotelRoom: HotelRoom;
};

const RecapHotelItem = ({
  selectedHotelRoomInfo,
  hotelRoom,
}: RecapHotelItemProps) => {
  const lang = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(lang, {
    style: "currency",
    currency: "EUR",
  });

  const bedLayout = hotelRoom.availableBedLayouts.find(
    (h) => h.id === selectedHotelRoomInfo.beds,
  );

  return (
    <div>
      <Text size="label2">
        <FormattedMessage
          id="tickets.checkout.recap.hotelRoomsPrice"
          values={{
            price: moneyFormatter.format(
              parseFloat(hotelRoom.price) * selectedHotelRoomInfo.numNights,
            ),
            perNight: moneyFormatter.format(parseFloat(hotelRoom.price)),
            taxRate: 0,
          }}
        />
        {" - "}
      </Text>
      <Text size="label1">{hotelRoom.name}</Text>{" "}
      <Text size="label2">
        {selectedHotelRoomInfo.checkin} - {selectedHotelRoomInfo.checkout} -{" "}
        {bedLayout.name}
      </Text>
    </div>
  );
};

type RecapItemProps = {
  selectedProductInfo: ProductState;
  product: TicketItem;
};

const RecapItem = ({ selectedProductInfo, product }: RecapItemProps) => {
  const lang = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(lang, {
    style: "currency",
    currency: "EUR",
  });
  const finalPrice = calculateProductPrice(
    product,
    selectedProductInfo.voucher,
  );
  const variationName = selectedProductInfo.variation
    ? product.variations.find((v) => v.id === selectedProductInfo.variation)
        ?.value
    : null;

  return (
    <div>
      {!!selectedProductInfo.voucher && (
        <Text decoration="line-through" size="label2">
          {moneyFormatter.format(parseFloat(product.defaultPrice))}
        </Text>
      )}{" "}
      <Text size="label2">
        <FormattedMessage
          id="tickets.checkout.recap.price"
          values={{
            price: moneyFormatter.format(finalPrice),
            taxRate: product.taxRate,
          }}
        />
        {" - "}
      </Text>
      <Text size="label1">
        {product.name} {variationName ? `(${variationName})` : ""}
      </Text>
    </div>
  );
};
