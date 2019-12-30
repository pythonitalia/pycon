/** @jsx jsx */
import { Button, Flex, Heading, Label, Radio } from "@theme-ui/components";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Alert } from "../alert";
import { TicketsForm } from "../tickets-form";
import { Ticket } from "../tickets-form/types";
import { InvoiceInformationState, SelectedProducts } from "./types";

type Props = {
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  default: boolean;
  invoiceInformation: InvoiceInformationState;
  onNextStep: () => void;
  addProduct: (id: string, variation?: string) => void;
  removeProduct: (id: string, variation?: string) => void;
  onUpdateIsBusiness: (isBusiness: boolean) => void;
};

const hasSelectedAtLeastOneProduct = (selectedProducts: SelectedProducts) =>
  Object.values(selectedProducts).length > 0;

export const TicketsSection: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
  onNextStep,
  invoiceInformation,
  onUpdateIsBusiness,
}) => {
  const [shouldShowNoTickets, setShouldShowNoTickets] = useState(false);

  const onContinue = () => {
    if (hasSelectedAtLeastOneProduct(selectedProducts)) {
      return onNextStep();
    }

    setShouldShowNoTickets(true);
  };

  return (
    <React.Fragment>
      <Heading sx={{ mb: 3 }}>
        <FormattedMessage id="tickets.heading" />
      </Heading>

      <Flex mb={3} sx={{ display: ["block", "flex"] }}>
        <Label
          sx={{
            width: "auto",
            mr: 3,
            mb: [3, 0],
            color: "green",
            fontWeight: "bold",
          }}
        >
          <Radio
            name="isBusiness"
            onChange={() => onUpdateIsBusiness(false)}
            checked={!invoiceInformation.isBusiness}
          />
          <FormattedMessage id="orderInformation.individualConsumer" />
        </Label>
        <Label
          sx={{
            width: "auto",
            mr: 3,
            color: "green",
            fontWeight: "bold",
          }}
        >
          <Radio
            name="isBusiness"
            onChange={() => onUpdateIsBusiness(true)}
            checked={invoiceInformation.isBusiness}
          />
          <FormattedMessage id="orderInformation.businessConsumer" />
        </Label>
      </Flex>

      {tickets && (
        <TicketsForm
          isBusiness={invoiceInformation.isBusiness}
          tickets={tickets}
          selectedProducts={selectedProducts}
          addProduct={addProduct}
          removeProduct={removeProduct}
        />
      )}

      {shouldShowNoTickets && (
        <Alert variant="alert">
          <FormattedMessage id="order.needToSelectProducts" />
        </Alert>
      )}

      <Button onClick={onContinue}>
        <FormattedMessage id="order.nextStep" />
      </Button>
    </React.Fragment>
  );
};
