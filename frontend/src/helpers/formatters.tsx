type Input = {
  fractionDigits?: number;
};

export const useMoneyFormatter = ({
  fractionDigits = undefined,
}: Input = {}) => {
  return new Intl.NumberFormat("en", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: fractionDigits,
    minimumFractionDigits: fractionDigits,
  });
};
