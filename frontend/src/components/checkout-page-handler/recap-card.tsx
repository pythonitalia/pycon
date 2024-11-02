import {
  CardPart,
  Heading,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import type { TicketItem } from "~/types";

import { calculateProductPrice } from "../tickets-page/review/prices";
import type { ProductState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

type Props = {
  productsById: { [id: number]: TicketItem };
};
export const RecapCard = ({ productsById }: Props) => {
  const {
    state: { selectedProducts },
  } = useCart();

  return (
    <div>
      <MultiplePartsCard
        openByDefault={false}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart contentAlign="left" id="heading">
          <Heading size={2}>
            <FormattedMessage id="tickets.checkout.recap" />
          </Heading>
        </CardPart>
        <CardPart background="milk" contentAlign="left" id="content">
          {Object.values(selectedProducts)
            .flatMap((nestedProducts) => nestedProducts.flat())
            .map((selectedProduct, index) => {
              const product = productsById[selectedProduct.id];
              return (
                <RecapItem
                  key={`${selectedProduct.id}-${index}`}
                  product={product}
                  selectedProductInfo={selectedProduct}
                />
              );
            })}
        </CardPart>
      </MultiplePartsCard>
    </div>
  );
};

type RecapItemProps = {
  selectedProductInfo: ProductState;
  product: TicketItem;
};

const RecapItem = ({ selectedProductInfo, product }: RecapItemProps) => {
  const lang = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(lang, {
    style: "currency",
    currency: "EUR",
  });
  const finalPrice = calculateProductPrice(
    product,
    selectedProductInfo.voucher,
  );
  const variationName = selectedProductInfo.variation
    ? product.variations.find((v) => v.id === selectedProductInfo.variation)
        ?.value
    : null;

  return (
    <div>
      {!!selectedProductInfo.voucher && (
        <Text decoration="line-through" size="label2">
          {moneyFormatter.format(Number.parseFloat(product.defaultPrice))}
        </Text>
      )}{" "}
      <Text size="label2">
        <FormattedMessage
          id="tickets.checkout.recap.price"
          values={{
            price: moneyFormatter.format(finalPrice),
            taxRate: product.taxRate,
          }}
        />
        {" - "}
      </Text>
      <Text size="label1">
        {product.name} {variationName ? `(${variationName})` : ""}
      </Text>
    </div>
  );
};
