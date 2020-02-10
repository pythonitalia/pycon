/** @jsx jsx */
import { Box, Button, Grid, Heading, Text } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../../context/language";
import { Link } from "../../link";
import { Ticket } from "../../tickets-form/types";
import { SelectedProducts } from "../types";
import { calculateProductPrice } from "./prices";
import { ReviewItem } from "./review-item";

type Props = {
  selectedProducts: SelectedProducts;
  productsById: {
    [x: string]: Ticket;
    [x: number]: Ticket;
  };
};

export const TicketsRecap: React.SFC<Props> = ({
  selectedProducts,
  productsById,
}) => {
  const lang = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(lang, {
    style: "currency",
    currency: "EUR",
  });

  const flatSelectedProducts = Object.values(selectedProducts).flat();

  if (flatSelectedProducts.length === 0) {
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
          <FormattedMessage id="orderReview.tickets" />
        </Heading>

        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {flatSelectedProducts.map((selectedProductInfo, index) => {
            const product = productsById[selectedProductInfo.id];
            const finalPrice = calculateProductPrice(
              product,
              selectedProductInfo.voucher,
            );
            const hasVoucher = !!selectedProductInfo.voucher;
            const variation = product.variations?.find(
              v => v.id === selectedProductInfo.variation,
            );

            return (
              <Box
                key={`${selectedProductInfo.id}-${index}`}
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
                  {product.name}
                  {variation && ` - ${variation.value}`}
                </Heading>

                {product.questions.length > 0 && (
                  <Fragment>
                    <Grid
                      sx={{
                        gridTemplateColumns: "1fr 1fr",
                        maxWidth: 400,
                        gridRowGap: 3,
                      }}
                    >
                      <ReviewItem
                        label={
                          <FormattedMessage id="orderReview.attendeeName" />
                        }
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

                      {hasVoucher && (
                        <ReviewItem
                          label={
                            <FormattedMessage id="orderReview.usingVoucher" />
                          }
                          value={selectedProductInfo.voucher!.code}
                        />
                      )}
                    </Grid>
                  </Fragment>
                )}

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
                      id={
                        hasVoucher
                          ? "orderReview.ticketPriceWithVoucher"
                          : "orderReview.ticketPrice"
                      }
                      values={{
                        basePrice: (
                          <Text
                            as="span"
                            sx={{
                              position: "relative",
                              "&:after": {
                                content: "''",

                                position: "absolute",
                                top: "50%",
                                left: "50%",

                                width: "100%",
                                height: "4px",
                                background: "black",

                                transform: "translate(-50%, -50%)",
                              },
                            }}
                          >
                            {moneyFormatter.format(
                              parseFloat(product.defaultPrice),
                            )}
                          </Text>
                        ),
                        finalPrice: (
                          <Text
                            as="span"
                            sx={{
                              position: "relative",
                              "&:after": {
                                content: "''",

                                display: hasVoucher ? "" : "none",

                                position: "absolute",
                                bottom: "-4px",
                                left: 0,

                                width: "100%",
                                height: "4px",
                                background: "green",
                              },
                            }}
                          >
                            {moneyFormatter.format(finalPrice)}{" "}
                            <FormattedMessage id="order.inclVat" />
                          </Text>
                        ),
                      }}
                    />
                  </Text>
                </Box>
              </Box>
            );
          })}
        </Box>

        <Link
          variant="button"
          sx={{
            mt: 5,
            px: 4,
            py: 2,
            textTransform: "uppercase",
            backgroundColor: "cinderella",
          }}
          href={`/${lang}/tickets/questions/`}
        >
          <FormattedMessage id="orderReview.edit" />
        </Link>
      </Box>
    </Box>
  );
};
