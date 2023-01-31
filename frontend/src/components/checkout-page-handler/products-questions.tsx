import { Spacer } from "@python-italia/pycon-styleguide";
import { Fragment } from "react";

import { TicketItem } from "~/types";

import { useCart } from "../tickets-page/use-cart";
import { AnswersCard } from "./answers-card";

type Props = {
  productsById: { [id: number]: TicketItem };
};

export const ProductsQuestions = ({ productsById }: Props) => {
  const {
    state: { selectedProducts },
  } = useCart();

  return (
    <>
      {Object.values(selectedProducts).map((selectedProducts, selectionIndex) =>
        selectedProducts
          .filter(
            (selectedProduct) =>
              productsById[selectedProduct.id].questions.length > 0,
          )
          .map((productUserInformation, localIndex) => (
            <Fragment
              key={`${selectionIndex}-${productUserInformation.id}-${localIndex}`}
            >
              <AnswersCard
                index={localIndex}
                openByDefault={selectionIndex === 0 && localIndex === 0}
                productUserInformation={productUserInformation}
                product={productsById[productUserInformation.id]}
              />
              <Spacer size="xs" />
            </Fragment>
          )),
      )}
    </>
  );
};
