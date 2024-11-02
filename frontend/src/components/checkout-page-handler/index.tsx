import { Heading, Section, Spacer } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useEffect } from "react";
import type {
  CurrentUserQueryResult,
  TicketItem,
  TicketsQueryResult,
} from "~/types";
import { useCart } from "../tickets-page/use-cart";
import { BillingCard } from "./billing-card";
import { CreateOrderBar } from "./create-order-bar";
import { PrivacyPolicy } from "./privacy-policy";
import { ProductsQuestions } from "./products-questions";
import { RecapCard } from "./recap-card";
import { useCreateOrder } from "./use-create-order";
import { VoucherCard } from "./voucher-card";

type Props = {
  products: TicketItem[];
  me: CurrentUserQueryResult["data"]["me"];
  conference: TicketsQueryResult["data"]["conference"];
};

export const CheckoutPageHandler = ({ products, me, conference }: Props) => {
  const productsById = Object.fromEntries(
    products.map((product) => [product.id, product]),
  );
  const { createOrder, isCreatingOrder, creationFailed, errors } =
    useCreateOrder({ userEmail: me?.email });
  const invoiceInformationErrors = errors?.invoiceInformation;
  const ticketsErrors = errors?.tickets;
  const {
    state: { selectedProducts },
    updateTicketInfo,
  } = useCart();

  useEffect(() => {
    Object.values(selectedProducts)
      .flat()
      .forEach((productUserInformation, index) => {
        const matchingErrors = ticketsErrors?.[index];
        updateTicketInfo({
          id: productUserInformation.id,
          index: productUserInformation.index,
          key: "errors",
          value: matchingErrors,
        });
      });
  }, [ticketsErrors]);

  return (
    <form
      onSubmit={(e) => e.preventDefault()}
      className="divide-y-3"
      autoComplete="off"
    >
      <Section spacingSize="xl" illustration="snakeTailUp">
        <Heading size="display2">
          <FormattedMessage id="tickets.checkout.title" />
        </Heading>
      </Section>
      <Section>
        <ProductsQuestions productsById={productsById} />
        <BillingCard
          invoiceInformationErrors={invoiceInformationErrors}
          me={me}
        />
        <Spacer size="xs" />
        <VoucherCard />
        <Spacer size="xs" />
        <RecapCard productsById={productsById} />
        <Spacer size="medium" />
        <PrivacyPolicy />
      </Section>
      <CreateOrderBar
        productsById={productsById}
        createOrder={createOrder}
        isCreatingOrder={isCreatingOrder}
        creationFailed={creationFailed}
      />
    </form>
  );
};
