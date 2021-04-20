import { loadStripe } from "@stripe/stripe-js";
import { useCallback, useContext, useState } from "react";
import { createContext, useEffect } from "react";

type StripeContextType = {
  stripe: any;
};

const StripeContext = createContext<StripeContextType>({
  stripe: null,
});

export const StripeProvider = ({ children }) => {
  const [stripe, setStripe] = useState(null);
  console.log(stripe);

  useEffect(() => {
    const load = async () => {
      const loadedStripe = await loadStripe("pk_test_1Tti9s1UY4Ot4NJXxWc6kdYg");
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
