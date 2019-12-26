/** @jsx jsx */
import { Button, Flex, Heading, Label, Radio } from "@theme-ui/components";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

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

export const TicketsSection: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
  onNextStep,
  invoiceInformation,
  onUpdateIsBusiness,
}) => (
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

    <Button onClick={onNextStep}>
      <FormattedMessage id="order.nextStep" />
    </Button>
  </React.Fragment>
);
