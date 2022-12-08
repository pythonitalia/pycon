/** @jsxRuntime classic */

/** @jsx jsx */
import { jsx } from "theme-ui";

import { GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { QuestionsSection } from "~/components/tickets-page/questions-section";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";

export const TicketsQuestionsPage = () => {
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
            router.push("/tickets/review/");
          }}
        />
      )}
    </TicketsPageWrapper>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export default TicketsQuestionsPage;
