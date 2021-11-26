/** @jsxRuntime classic */

/** @jsx jsx */
import moment from "moment";
import { FormattedMessage } from "react-intl";
import { Box, Grid, jsx, Text } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";

import { AddHotelRoom } from "./add-hotel-room";
import { AddProductWithVariation } from "./add-product-with-variation";
import { AddRemoveProduct } from "./add-remove-product";
import { ProductSelectedVariationsList } from "./product-selected-variations-list";
import { Ticket } from "./types";

type SelectedProduct = {
  id: string;
  variation?: string;
};

type ProductRowProps = {
  className?: string;
  ticket: Ticket;
  quantity?: number;
  hotel?: boolean;
  conferenceStart?: string;
  conferenceEnd?: string;
  addProduct?: (ticketId: string, variation?: string) => void;
  removeProduct?: (ticketId: string) => void;
  addHotelRoom?: (
    id: string,
    checkin: moment.Moment,
    checkout: moment.Moment,
  ) => void;
  removeHotelRoom?: (index: number) => void;
  selectedProducts?: {
    [id: string]: SelectedProduct[];
  };
};

export const ProductRow = ({
  className,
  hotel,
  ticket,
  selectedProducts,
  conferenceStart,
  conferenceEnd,
  addHotelRoom,
  quantity,
  addProduct,
  removeProduct,
}: ProductRowProps) => {
  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const hasVariation = ticket.variations && ticket.variations.length > 0;

  return (
    <Box sx={{ my: 4 }} className={className}>
      <Grid
        sx={{
          gridTemplateColumns: ["1fr", hotel ? "1fr 370px" : "1fr 180px"],
        }}
      >
        <Box>
          <Text as="label" variant="label">
            {ticket.name}
          </Text>

          <Text>
            <FormattedMessage
              id={hotel ? "order.hotelPrice" : "order.price"}
              values={{
                price: (
                  <Text as="span" sx={{ fontWeight: "bold" }}>
                    {ticket.defaultPrice}
                  </Text>
                ),
              }}
            />
            <Text
              as="span"
              sx={{
                fontSize: 1,
                ml: 1,
              }}
            >
              <FormattedMessage id="order.inclVat" />
            </Text>
          </Text>

          <Text>{ticket.description}</Text>
          {ticket.availableUntil && (
            <Text>
              <FormattedMessage
                id="order.availableUntil"
                values={{
                  date: (
                    <strong>
                      {dateFormatter.format(new Date(ticket.availableUntil))}
                    </strong>
                  ),
                }}
              />
            </Text>
          )}
        </Box>

        {ticket.soldOut && (
          <Text
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-end",
              fontSize: 3,
              fontWeight: "bold",
            }}
          >
            <FormattedMessage id="order.soldout" />
          </Text>
        )}

        {!ticket.soldOut && hotel && (
          <AddHotelRoom
            conferenceStart={conferenceStart}
            conferenceEnd={conferenceEnd}
            addRoom={(checkin, checkout) =>
              addHotelRoom && addHotelRoom(ticket.id, checkin, checkout)
            }
          />
        )}

        {!ticket.soldOut && !hotel && !hasVariation && (
          <AddRemoveProduct
            quantity={quantity!}
            increase={() => addProduct && addProduct(ticket.id)}
            decrease={() => removeProduct && removeProduct(ticket.id)}
          />
        )}

        {!ticket.soldOut && !hotel && hasVariation && (
          <AddProductWithVariation
            addVariation={(variation: string) =>
              addProduct && addProduct(ticket.id, variation)
            }
            ticket={ticket}
          />
        )}
      </Grid>

      {hasVariation && (
        <ProductSelectedVariationsList
          product={ticket}
          selectedProducts={selectedProducts}
          removeProduct={removeProduct}
        />
      )}
    </Box>
  );
};
