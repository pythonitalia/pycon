/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Heading, Text } from "@theme-ui/components";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCountries } from "../../helpers/use-countries";
import { Ticket } from "../tickets-form/types";
import { CreateOrderButtons } from "./create-order-buttons";
import { InvoiceInformationState, OrderState } from "./types";

type Props = {
  state: OrderState;
  tickets: Ticket[];
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

const ReviewItem = ({
  label,
  value,
}: {
  label: string | React.ReactElement;
  value: string | React.ReactElement;
}) => (
  <li
    sx={{
      mt: 1,
    }}
  >
    <Text
      as="p"
      sx={{
        fontWeight: "bold",
      }}
    >
      {label}
    </Text>
    <Text as="p">{value}</Text>
  </li>
);

export const ReviewOrder: React.SFC<Props> = ({ state, tickets, email }) => {
  const { invoiceInformation, selectedProducts } = state!;
  const productsById = Object.fromEntries(
    tickets!.map(product => [product.id, product]),
  );
  const countries = useCountries();
  const totalAmount = Object.values(selectedProducts)
    .flat()
    .reduce((p, c) => p + parseFloat(productsById[c.id].defaultPrice), 0);

  const isBusiness = state!.invoiceInformation.isBusiness === "true";

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
              value={outputValue}
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
                    justifyContent: "space-between",
                    alignItems: "center",
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
                      <FormattedMessage id="orderReview.inclVat" />
                    </Text>
                  </Text>
                </Flex>
                {product.questions.length > 0 && (
                  <Box
                    as="ul"
                    sx={{
                      pl: 4,
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
                      console.log("question.options", question.options);
                      const isSelect = question.options.length > 0;
                      const answer = selectedProductInfo.answers[question.id];

                      return (
                        <ReviewItem
                          key={question.id}
                          label={question.name}
                          value={
                            isSelect
                              ? question.options.find(o => o.id === answer)!
                                  .name
                              : answer
                          }
                        />
                      );
                    })}
                  </Box>
                )}
              </li>
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
