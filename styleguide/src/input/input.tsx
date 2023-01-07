import clsx from "clsx";
import React from "react";
import { InputBar } from "./input-bar";

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  errors?: (string | React.ReactNode)[];
};

export const Input = ({ errors, ...props }: Props) => {
  const { value, maxLength } = props;
  const errorsOrEmpty = (errors ?? []).filter((e) => !!e);
  const hasError = errorsOrEmpty.length > 0;

  return (
    <div>
      <input
        {...props}
        className={clsx(
          "w-full font-sans text-md bg-transparent placeholder:text-grey-250 placeholder:font-sans border-b border-black py-2 transition-colors",
          "outline-none focus:border-green font-medium leading-2",
          {
            "border-red": hasError,
            "border-black": !hasError,
          }
        )}
      />
      <InputBar errors={errorsOrEmpty} value={value} maxLength={maxLength} />
    </div>
  );
};
