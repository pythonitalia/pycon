import { loadStripe } from "@stripe/stripe-js";
import { createContext, useContext, useEffect, useState } from "react";

import { STRIPE_KEY } from "~/helpers/config";

type StripeContextType = {
  stripe: any;
};

const StripeContext = createContext<StripeContextType>({
  stripe: null,
});

export const StripeProvider = ({ children }) => {
  const [stripe, setStripe] = useState(null);

  useEffect(() => {
    const load = async () => {
      const loadedStripe = await loadStripe(STRIPE_KEY);
      setStripe(loadedStripe);
    };
    load();
  }, []);

  return (
    <StripeContext.Provider
      value={{
        stripe,
      }}
    >
      {children}
    </StripeContext.Provider>
  );
};

export const useStripe = () => {
  const { stripe } = useContext(StripeContext);
  const redirectToCheckout = (sessionId) => {
    return stripe.redirectToCheckout({
      sessionId: sessionId,
    });
  };
  return {
    stripe,
    redirectToCheckout,
  };
};
