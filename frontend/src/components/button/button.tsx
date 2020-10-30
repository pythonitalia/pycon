/** @jsxRuntime classic */
/** @jsx jsx */
import { useEffect, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Button as ThemeButton, jsx } from "theme-ui";

type ButtonProps = {
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "reset" | "submit";
  variant?: string;
  onClick?: () => void;
};

const useInterval = (callback: () => void, delay: number) => {
  const savedCallback = useRef<() => void>();

  useEffect(() => {
    savedCallback.current = callback;
  });

  useEffect(() => {
    function tick() {
      savedCallback.current();
    }

    const id = setInterval(tick, delay);
    return () => clearInterval(id);
  }, [delay]);
};

export const Button: React.SFC<ButtonProps> = ({
  disabled,
  loading,
  children,
  ...props
}) => {
  const clocks = [
    "🕐",
    "🕑",
    "🕒",
    "🕓",
    "🕔",
    "🕕",
    "🕖",
    "🕗",
    "🕘",
    "🕙",
    "🕚",
    "🕛",
  ];

  const [count, setCount] = useState(0);

  useInterval(
    () => {
      setCount(count + 1);
    },
    loading ? 100 : null,
  );

  return (
    <ThemeButton disabled={disabled || loading} {...props}>
      {loading ? (
        <FormattedMessage
          id="global.button.loading"
          values={{
            emoji: clocks[count % clocks.length],
          }}
        />
      ) : (
        children
      )}
    </ThemeButton>
  );
};
