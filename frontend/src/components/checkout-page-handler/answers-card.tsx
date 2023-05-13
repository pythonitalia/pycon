import {
  MultiplePartsCard,
  CardPart,
  Heading,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

type Props = {
  openByDefault: boolean;
  title: string;
  children: React.ReactNode;
};

export const AnswersCard = ({ openByDefault, children, title }: Props) => {
  return (
    <MultiplePartsCard
      openByDefault={openByDefault}
      clickablePart="heading"
      expandTarget="content"
    >
      <CardPart
        iconBackground="pink"
        icon="tickets"
        contentAlign="left"
        id="heading"
        openLabel={<FormattedMessage id="tickets.checkout.openAnswerCard" />}
      >
        <Heading size={2}>{title}</Heading>
      </CardPart>
      <CardPart id="content" contentAlign="left" background="milk">
        {children}
      </CardPart>
    </MultiplePartsCard>
  );
};
