/** @jsx jsx */
import { Box, Button, Flex, Grid, Heading } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../../context/language";
import { useCountries } from "../../../helpers/use-countries";
import { Link } from "../../link";
import { InvoiceInformationState } from "../types";
import { ReviewItem } from "./review-item";

const INVOICE_FIELDS: {
  key: keyof InvoiceInformationState;
  label: string;
}[] = [
  { key: "companyName", label: "orderReview.companyName" },
  { key: "name", label: "orderReview.name" },
  { key: "vatId", label: "orderReview.vatId" },
  { key: "fiscalCode", label: "orderReview.fiscalCode" },
  { key: "address", label: "orderReview.address" },
  { key: "zipCode", label: "orderReview.zipCode" },
  { key: "city", label: "orderReview.city" },
  { key: "country", label: "orderReview.country" },
];

type Props = {
  data: InvoiceInformationState;
};

export const InvoiceInformation: React.SFC<Props> = ({ data }) => {
  const countries = useCountries();
  const lang = useCurrentLanguage();
  const isBusiness = data.isBusiness;

  return (
    <Box
      sx={{
        py: 5,
        borderTop: "primary",
      }}
    >
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
          <FormattedMessage id="orderReview.invoiceInformation" />
        </Heading>

        <Grid
          sx={{
            gridTemplateColumns: "1fr 1fr",
            gridRowGap: 3,
            maxWidth: "400px",
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
                id={`orderReview.isBusiness.${data.isBusiness}`}
              />
            }
          />

          {INVOICE_FIELDS.map(field => {
            const inputValue = data[field.key];
            let outputValue = inputValue;

            switch (field.key) {
              case "country":
                outputValue = countries.find(c => c.value === inputValue)
                  ?.label;
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
        </Grid>

        <Link
          variant="button"
          sx={{
            mt: 5,
            px: 4,
            py: 2,
            textTransform: "uppercase",
            backgroundColor: "cinderella",
          }}
          href={`/${lang}/tickets/information/`}
        >
          <FormattedMessage id="orderReview.edit" />
        </Link>
      </Box>
    </Box>
  );
};
