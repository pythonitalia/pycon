/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Button as ThemeButton, jsx } from "theme-ui";

import { AnimatedEmoji } from "../animated-emoji";

type ButtonProps = {
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "reset" | "submit";
  variant?: string;
  onClick?: () => void;
  sx?: any;
};

export const Button = ({
  disabled,
  loading,
  children,
  ...props
}: React.PropsWithChildren<ButtonProps>) => {
  return (
    <ThemeButton disabled={disabled || loading} {...props}>
      {loading ? (
        <FormattedMessage
          id="global.button.loading"
          values={{
            emoji: <AnimatedEmoji play={loading} />,
          }}
        />
      ) : (
        children
      )}
    </ThemeButton>
  );
};
