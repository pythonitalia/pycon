import { Heading, Spacer } from "@python-italia/pycon-styleguide";
import { Fragment } from "react";

import { TicketItem } from "~/types";

import { ProductQuestionnaire } from "../product-questionnaire";
import { useCart } from "../tickets-page/use-cart";
import { AnswersCard } from "./answers-card";

type Props = {
  productsById: { [id: number]: TicketItem };
};

export const ProductsQuestions = ({ productsById }: Props) => {
  const {
    state: { selectedProducts },
  } = useCart();
  const { updateTicketInfo, updateQuestionAnswer } = useCart();

  return (
    <>
      {Object.entries(selectedProducts)
        .filter(([productId]) => productsById[productId].questions.length > 0)
        .map(([productId, selection]) => {
          return (
            <Fragment>
              <AnswersCard
                title={productsById[productId].name}
                openByDefault={true}
              >
                {selection.map((productUserInformation, index) => (
                  <>
                    <Heading size={4}>
                      {productsById[productId].name} #{index + 1}
                    </Heading>
                    <Spacer size="2md" />
                    <ProductQuestionnaire
                      index={index}
                      productUserInformation={productUserInformation}
                      product={productsById[productId]}
                      updateTicketInfo={updateTicketInfo}
                      updateQuestionAnswer={updateQuestionAnswer}
                    />
                    {index !== selection.length - 1 && <Spacer size="large" />}
                  </>
                ))}
              </AnswersCard>
              <Spacer size="xs" />
            </Fragment>
          );
        })}
    </>
  );
};
