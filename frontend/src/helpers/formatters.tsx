import { useCurrentLanguage } from "~/locale/context";

type Input = {
  fractionDigits?: number;
};

export const useMoneyFormatter = ({
  fractionDigits = undefined,
}: Input = {}) => {
  const language = useCurrentLanguage();
  return new Intl.NumberFormat(language, {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: fractionDigits,
    minimumFractionDigits: fractionDigits,
  });
};
