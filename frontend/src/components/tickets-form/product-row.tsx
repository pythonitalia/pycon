/** @jsxRuntime classic */

/** @jsx jsx */
import moment from "moment";
import { FormattedMessage } from "react-intl";
import { Box, Grid, jsx, Text } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { CurrentUserQueryResult, TicketType, TicketItem } from "~/types";

import { AddHotelRoom } from "./add-hotel-room";
import { AddMembershipSubscription } from "./add-membership-subscription";
import { AddProductWithVariation } from "./add-product-with-variation";
import { AddRemoveProduct } from "./add-remove-product";
import { ProductSelectedVariationsList } from "./product-selected-variations-list";

type SelectedProduct = {
  id: string;
  variation?: string;
};

type ProductRowProps = {
  className?: string;
  ticket: TicketItem;
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
  me: CurrentUserQueryResult["data"]["me"];
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
  me,
}: ProductRowProps) => {
  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const hasVariation = ticket.variations && ticket.variations.length > 0;
  const isMembershipProduct = ticket.type === TicketType.Association;

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
              <FormattedMessage
                id={hotel ? "order.hotelNoVat" : "order.inclVat"}
                values={{
                  taxRate: ticket.taxRate,
                }}
              />
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

        {!ticket.soldOut && !hotel && !hasVariation && !isMembershipProduct && (
          <div>
            <AddRemoveProduct
              quantity={quantity!}
              increase={() => addProduct && addProduct(ticket.id)}
              decrease={() => removeProduct && removeProduct(ticket.id)}
            />

            {ticket.quantityLeft !== null && (
              <Text
                sx={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "flex-end",
                  textAlign: "right",
                  mt: 2,
                  fontSize: 2,
                }}
              >
                <FormattedMessage
                  id="order.ticketsLeft"
                  values={{
                    count: ticket.quantityLeft,
                  }}
                />{" "}
                <span sx={{ fontSize: "1.2em", ml: 1 }}>🎟️</span>
              </Text>
            )}
          </div>
        )}

        {!ticket.soldOut && isMembershipProduct && (
          <AddMembershipSubscription
            me={me}
            added={quantity === 1}
            add={() => addProduct?.(ticket.id)}
            remove={() => removeProduct?.(ticket.id)}
          />
        )}

        {!ticket.soldOut && !hotel && hasVariation && (
          <AddProductWithVariation
            addVariation={(variation: string) =>
              addProduct?.(ticket.id, variation)
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
