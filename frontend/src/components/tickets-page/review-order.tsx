/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Flex, Heading, Text } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../context/language";
import { HotelRoom } from "../../generated/graphql-backend";
import { useCountries } from "../../helpers/use-countries";
import { Ticket } from "../tickets-form/types";
import { CreateOrderButtons } from "./create-order-buttons";
import { ReviewItem } from "./review-item";
import { InvoiceInformationState, OrderState } from "./types";

type Props = {
  state: OrderState;
  tickets: Ticket[];
  hotelRooms: HotelRoom[];
  email: string;
} & RouteComponentProps;

const INVOICE_FIELDS: {
  key: keyof InvoiceInformationState;
  label: string;
}[] = [
  {
    key: "companyName",
    label: "orderReview.companyName",
  },
  {
    key: "name",
    label: "orderReview.name",
  },
  {
    key: "vatId",
    label: "orderReview.vatId",
  },
  {
    key: "fiscalCode",
    label: "orderReview.fiscalCode",
  },
  {
    key: "address",
    label: "orderReview.address",
  },
  {
    key: "zipCode",
    label: "orderReview.zipCode",
  },
  {
    key: "city",
    label: "orderReview.city",
  },
  {
    key: "country",
    label: "orderReview.country",
  },
];

const calculateTotalAmount = (
  state: OrderState,
  productsById: {
    [x: string]: Ticket;
    [x: number]: Ticket;
  },
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  },
) => {
  const ticketsPrice = Object.values(state.selectedProducts)
    .flat()
    .reduce((p, c) => p + parseFloat(productsById[c.id].defaultPrice), 0);
  const hotelRoomsPrice = Object.values(state.selectedHotelRooms)
    .flat()
    .reduce(
      (p, c) => p + parseFloat(hotelRoomsById[c.id].price) * c.numNights,
      0,
    );
  return ticketsPrice + hotelRoomsPrice;
};

export const ReviewOrder: React.SFC<Props> = ({
  state,
  tickets,
  hotelRooms,
  email,
}) => {
  const { invoiceInformation, selectedProducts, selectedHotelRooms } = state!;
  const productsById = Object.fromEntries(
    tickets!.map(product => [product.id, product]),
  );
  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map(room => [room.id, room]),
  );
  const countries = useCountries();
  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);

  const isBusiness = state!.invoiceInformation.isBusiness;

  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    month: "long",
    day: "2-digit",
  });

  return (
    <Box>
      <Heading as="h1" mb={2}>
        <FormattedMessage id="orderReview.heading" />
      </Heading>

      <Heading as="h2" my={3}>
        <FormattedMessage id="orderReview.invoiceInformation" />
      </Heading>

      <Box
        as="ul"
        sx={{
          listStyle: "none",
        }}
      >
        <ReviewItem
          sx={{
            mb: 2,
          }}
          label={<FormattedMessage id="orderReview.isBusiness" />}
          value={
            <FormattedMessage
              id={`orderReview.isBusiness.${invoiceInformation.isBusiness}`}
            />
          }
        />

        {INVOICE_FIELDS.map(field => {
          const inputValue = invoiceInformation[field.key];
          let outputValue = inputValue;

          switch (field.key) {
            case "country":
              outputValue = countries.find(c => c.value === inputValue)?.label;
              break;
            case "companyName":
              if (!isBusiness) {
                return null;
              }
              break;
          }

          if (outputValue === "") {
            return null;
          }

          return (
            <ReviewItem
              key={field.key}
              sx={{
                mb: 2,
              }}
              label={<FormattedMessage id={field.label} />}
              value={outputValue as string}
            />
          );
        })}
      </Box>

      <Heading as="h2" my={3}>
        <FormattedMessage id="orderReview.tickets" />
      </Heading>

      <Box
        as="ul"
        sx={{
          listStyle: "none",
        }}
      >
        {Object.values(selectedProducts)
          .flat()
          .map((selectedProductInfo, index) => {
            const product = productsById[selectedProductInfo.id];

            return (
              <li
                key={`${selectedProductInfo.id}-${index}`}
                sx={{
                  my: 3,
                }}
              >
                <Flex
                  sx={{
                    flexDirection: ["column", "row"],
                    justifyContent: "space-between",
                    alignItems: ["flex-start", "center"],
                  }}
                >
                  <Heading as="h3">{product.name}</Heading>
                  <Text>
                    <Text
                      as="span"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      {product.defaultPrice}€
                    </Text>{" "}
                    <Text
                      sx={{
                        fontSize: 1,
                      }}
                      as="span"
                    >
                      <FormattedMessage id="order.inclVat" />
                    </Text>
                  </Text>
                </Flex>
                {product.questions.length > 0 && (
                  <Box
                    as="ul"
                    sx={{
                      pl: [2, 4],
                      listStyle: "none",
                    }}
                  >
                    <ReviewItem
                      label={<FormattedMessage id="orderReview.attendeeName" />}
                      value={selectedProductInfo.attendeeName}
                    />

                    <ReviewItem
                      label={
                        <FormattedMessage id="orderReview.attendeeEmail" />
                      }
                      value={selectedProductInfo.attendeeEmail}
                    />

                    {product.questions.map(question => {
                      const isSelect = question.options.length > 0;
                      const answer = selectedProductInfo.answers[question.id];
                      const convertedSelectAnswerOrAnswer = isSelect
                        ? question.options.find(o => o.id === answer)?.name
                        : answer;

                      return (
                        <ReviewItem
                          key={question.id}
                          label={question.name}
                          value={convertedSelectAnswerOrAnswer}
                        />
                      );
                    })}
                  </Box>
                )}
              </li>
            );
          })}
      </Box>

      <Heading as="h2" my={3}>
        <FormattedMessage id="orderReview.hotelRooms" />
      </Heading>

      <Box
        as="ul"
        sx={{
          listStyle: "none",
        }}
      >
        {Object.values(selectedHotelRooms)
          .flat()
          .map((selectedRoomInfo, index) => {
            const room = hotelRoomsById[selectedRoomInfo.id];
            return (
              <Box
                sx={{
                  my: 3,
                }}
                key={`${selectedRoomInfo.id}-${index}`}
              >
                <Flex
                  sx={{
                    flexDirection: ["column", "row"],
                    justifyContent: "space-between",
                    alignItems: ["flex-start", "center"],
                  }}
                >
                  <Heading as="h3">{room.name}</Heading>
                  <Text>
                    <Text
                      as="span"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      {room.price}€
                    </Text>{" "}
                    x{selectedRoomInfo.numNights}{" "}
                    <FormattedMessage
                      id={
                        selectedRoomInfo.numNights === 1
                          ? "orderReview.night"
                          : "orderReview.nights"
                      }
                    />{" "}
                    <Text
                      sx={{
                        fontSize: 1,
                      }}
                      as="span"
                    >
                      <FormattedMessage id="order.inclVat" />
                    </Text>
                  </Text>
                </Flex>

                <Box
                  as="ul"
                  sx={{
                    pl: [2, 4],
                    listStyle: "none",
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
                </Box>
              </Box>
            );
          })}
      </Box>

      <Flex
        sx={{
          borderTop: "primary",
          justifyContent: "space-between",
          alignItems: "center",
          mt: 3,
          py: 2,
        }}
      >
        <Text as="h2">
          <FormattedMessage id="orderReview.total" />
        </Text>
        <Text
          sx={{
            fontWeight: "bold",
          }}
        >
          {totalAmount}€
        </Text>
      </Flex>

      <CreateOrderButtons email={email} state={state} />
    </Box>
  );
};
