import { useLoginState } from "~/components/profile/hooks";
import { Tickets } from "~/components/tickets-page/tickets";
import {
  CartContext,
  createCartContext,
} from "~/components/tickets-page/use-cart";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useCurrentLanguage } from "~/locale/context";
import {
  CheckoutCategory,
  queryCheckoutSection,
  useCheckoutSectionQuery,
} from "~/types";

type Props = {
  visibleCategories: CheckoutCategory[];
};

export const CheckoutSection = ({ visibleCategories }: Props) => {
  const language = useCurrentLanguage();
  const {
    data: {
      conference,
      conference: { tickets, hotelRooms },
    },
  } = useCheckoutSectionQuery({
    variables: {
      conference: process.env.conferenceCode,
      language: language,
    },
  });
  const [isLoggedIn] = useLoginState();
  const { user: me } = useCurrentUser({
    skip: !isLoggedIn,
  });
  const cartContext = createCartContext();

  return (
    <CartContext.Provider value={cartContext}>
      <Tickets
        products={tickets}
        hotelRooms={hotelRooms}
        conference={conference}
        me={me}
        business={false}
        visibleCategories={visibleCategories}
        showHeadings={false}
      />
    </CartContext.Provider>
  );
};

CheckoutSection.dataFetching = (client, locale) => {
  return [
    queryCheckoutSection(client, {
      conference: process.env.conferenceCode,
      language: locale,
    }),
  ];
};
