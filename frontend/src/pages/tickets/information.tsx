/** @jsxRuntime classic */

/** @jsx jsx */
import { jsx } from "theme-ui";

import { useRouter } from "next/router";

import { InformationSection } from "~/components/tickets-page/information-section";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";

export const TicketsInformationPage = () => {
  const router = useRouter();

  const { state, updateInformation } = useCart();

  return (
    <TicketsPageWrapper>
      {({ tickets }) => (
        <InformationSection
          onUpdateInformation={updateInformation}
          invoiceInformation={state.invoiceInformation}
          onNextStep={() => {
            const productIds = Object.values(state.selectedProducts).flatMap(
              (instances) => instances.map((product) => product.id),
            );

            const selectedProductsInfo = tickets.filter((ticket) =>
              productIds.includes(ticket.id),
            );

            const numberOfQuestions = selectedProductsInfo
              .map((info) => info.questions.length)
              .reduce((sum, length) => sum + length, 0);

            if (numberOfQuestions > 0) {
              router.push("/tickets/questions/");
            } else {
              router.push("/tickets/review/");
            }
          }}
        />
      )}
    </TicketsPageWrapper>
  );
};

export default TicketsInformationPage;
