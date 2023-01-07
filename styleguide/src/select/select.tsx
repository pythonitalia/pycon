import clsx from "clsx";
import React from "react";
import { ArrowDownIcon } from "../icons/arrow-down";
import { Spacer } from "../spacer";
import { Text } from "../text";

type Props = React.InputHTMLAttributes<HTMLSelectElement> & {
  errors?: (string | React.ReactNode)[];
  children: React.ReactNode;
};

export const Select = ({ errors, children, ...props }: Props) => {
  const errorsOrEmpty = (errors ?? []).filter((e) => !!e);
  const hasError = errorsOrEmpty.length > 0;

  return (
    <div>
      <div className="relative">
        <select
          {...props}
          className={clsx(
            "w-full font-sans text-md bg-transparent placeholder:text-grey-250 placeholder:font-sans border-b py-2 transition-colors",
            "appearance-none outline-none focus:border-green font-medium leading-2",
            {
              "border-red": hasError,
              "border-black": !hasError,
              "text-grey-250": props.value === "",
            }
          )}
        >
          {children}
        </select>
        <ArrowDownIcon className="absolute top-1/2 -translate-y-1/2 right-3" />
      </div>
      <Spacer size="xs" />
      <Text as="p" size="label4" color="error" uppercase>
        {errorsOrEmpty.join(", ")}
      </Text>
    </div>
  );
};
