/** @jsx jsx */

import { useRouter } from "next/router";
import { jsx } from "theme-ui";

import { QuestionsSection } from "~/components/tickets-page/questions-section";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { useCurrentLanguage } from "~/locale/context";

export const TicketsQuestionsPage = () => {
  const language = useCurrentLanguage();
  const router = useRouter();

  const { state, updateTicketInfo, updateQuestionAnswer } = useCart();

  return (
    <TicketsPageWrapper>
      {({ tickets }) => (
        <QuestionsSection
          tickets={tickets}
          updateTicketInfo={updateTicketInfo}
          updateQuestionAnswer={updateQuestionAnswer}
          selectedProducts={state.selectedProducts}
          onNextStep={() => {
            router.push(
              "/[lang]/tickets/review/",
              `/${language}/tickets/review/`,
            );
          }}
        />
      )}
    </TicketsPageWrapper>
  );
};

export default TicketsQuestionsPage;
