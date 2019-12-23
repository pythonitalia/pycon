/** @jsx jsx */
import { Button, Heading } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { TicketsForm } from "../tickets-form";
import { Ticket } from "../tickets-form/types";
import { SelectedProducts } from "./types";

type Props = {
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  default: boolean;
  onNextStep: () => void;
  addProduct: (id: string, variation?: string) => void;
  removeProduct: (id: string, variation?: string) => void;
};

export const TicketsSection: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
  onNextStep,
}) => (
  <React.Fragment>
    <Heading sx={{ mb: 3 }}>
      <FormattedMessage id="tickets.heading" />
    </Heading>

    {tickets && (
      <TicketsForm
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
