import { MultiplePartsCard, CardPart } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { TicketItem } from "~/types";

import { ProductQuestionnaire } from "../product-questionnaire";
import { ProductState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

type Props = {
  openByDefault: boolean;
  productUserInformation: ProductState;
  product: TicketItem;
  index: number;
};

export const AnswersCard = ({
  openByDefault,
  productUserInformation,
  product,
  index,
}: Props) => {
  const { updateTicketInfo, updateQuestionAnswer } = useCart();
  const cardTitle =
    product.admission && productUserInformation.attendeeName ? (
      <FormattedMessage
        id="tickets.checkout.answerCardAdmissionTitle"
        values={{
          attendeeName: productUserInformation.attendeeName,
        }}
      />
    ) : (
      product.name
    );

  return (
    <MultiplePartsCard
      openByDefault={openByDefault}
      clickablePart="heading"
      expandTarget="content"
    >
      <CardPart
        iconBackground="pink"
        title={cardTitle}
        icon="ticket"
        contentAlign="left"
        id="heading"
        openLabel={<FormattedMessage id="tickets.checkout.openAnswerCard" />}
      />
      <CardPart id="content" contentAlign="left" noBg>
        <ProductQuestionnaire
          index={index}
          productUserInformation={productUserInformation}
          product={product}
          updateTicketInfo={updateTicketInfo}
          updateQuestionAnswer={updateQuestionAnswer}
        />
      </CardPart>
    </MultiplePartsCard>
  );
};
