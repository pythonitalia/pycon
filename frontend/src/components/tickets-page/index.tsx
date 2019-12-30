/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps, Router } from "@reach/router";
import { Box, Text } from "@theme-ui/components";
import React, { useCallback, useContext, useReducer } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  TicketsQuery,
  TicketsQueryVariables,
} from "../../generated/graphql-backend";
import { MetaTags } from "../meta-tags";
import { InformationSection } from "./information";
import { QuestionsSection } from "./questions";
import { reducer } from "./reducer";
import { ReviewOrder } from "./review-order";
import { TicketsSection } from "./tickets";
import TICKETS_QUERY from "./tickets.graphql";

export const TicketsPage: React.SFC<RouteComponentProps> = props => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();

  const { loading, error, data } = useQuery<
    TicketsQuery,
    TicketsQueryVariables
  >(TICKETS_QUERY, {
    variables: {
      conference: conferenceCode,
      language,
    },
  });

  const [state, dispatcher] = useReducer(reducer, {
    selectedProducts: {},
    invoiceInformation: {
      isBusiness: false,
      companyName: "",
      name: "",
      vatId: "",
      address: "",
      zipCode: "",
      city: "",
      country: "",
      fiscalCode: "",
    },
  });

  if (error) {
    throw new Error(error.message);
  }

  const tickets = data?.conference.tickets || [];

  const addProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "incrementProduct",
      id,
      variation,
    });

  const removeProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "decrementProduct",
      id,
      variation,
    });

  const updateQuestionAnswer = useCallback(
    ({ id, index, question, answer }) =>
      dispatcher({
        type: "updateTicketAnswer",
        id,
        index,
        question,
        answer,
      }),
    [],
  );

  const updateTicketInfo = useCallback(
    ({ id, index, key, value }) =>
      dispatcher({
        type: "updateTicketInfo",
        id,
        index,
        key,
        value,
      }),
    [],
  );

  const updateIsBusiness = useCallback(
    (isBusiness: boolean) =>
      dispatcher({
        type: "updateIsBusiness",
        isBusiness,
      }),
    [],
  );

  const goToQuestionsOrReview = () => {
    const productIds = Object.values(
      state.selectedProducts,
    ).flatMap(instances => instances.map(product => product.id));

    const selectedProductsInfo = tickets.filter(ticket =>
      productIds.includes(ticket.id),
    );

    const numberOfQuestions = selectedProductsInfo
      .map(info => info.questions.length)
      .reduce((sum, length) => sum + length, 0);

    if (numberOfQuestions > 0) {
      props.navigate!("questions");
    } else {
      props.navigate!("review");
    }
  };

  return (
    <Box>
      <FormattedMessage id="tickets.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Text>
            <FormattedMessage id="tickets.loading" />
          </Text>
        )}

        {!loading && (
          <Router>
            <TicketsSection
              default={true}
              tickets={tickets}
              selectedProducts={state.selectedProducts}
              addProduct={addProduct}
              removeProduct={removeProduct}
              invoiceInformation={state.invoiceInformation}
              onUpdateIsBusiness={updateIsBusiness}
              onNextStep={() => props.navigate!("information")}
            />
            <InformationSection
              path="information"
              onUpdateInformation={invoiceData =>
                dispatcher({
                  type: "updateInvoiceInformation",
                  data: invoiceData,
                })
              }
              invoiceInformation={state.invoiceInformation}
              onNextStep={goToQuestionsOrReview}
            />
            <QuestionsSection
              path="questions"
              tickets={tickets}
              updateTicketInfo={updateTicketInfo}
              updateQuestionAnswer={updateQuestionAnswer}
              selectedProducts={state.selectedProducts}
              onNextStep={() => props.navigate!("review")}
            />

            <ReviewOrder
              email={data?.me.email!}
              tickets={tickets}
              state={state}
              path="review"
            />
          </Router>
        )}
      </Box>
    </Box>
  );
};
