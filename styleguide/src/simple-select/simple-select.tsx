import clsx from "clsx";
import React from "react";
import { ArrowDownIcon } from "../icons/arrow-down";

export type Option = {
  value: string;
  label: string;
};

type Props = {
  options: Option[];
  placeholder?: string | React.ReactNode;
  value?: string;
  className?: string;
  onChange?: (e: any) => void;
  disabled?: boolean;
};

export const SimpleSelect = ({
  options,
  placeholder,
  className,
  value = "",
  onChange,
  disabled = false,
}: Props) => {
  return (
    <div className="relative w-full h-full">
      <select
        disabled={disabled}
        onChange={onChange}
        className={clsx(
          "w-full h-full bg-transparent uppercase font-sans font-bold text-base leading-1 appearance-none",
          "pr-5",
          {
            "text-grey-250": value === "",
          },
          className
        )}
        value={value}
      >
        {placeholder && (
          <option value="" disabled={true}>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {!disabled && (
        <div className="absolute top-1/2 -translate-y-1/2 right-3 lg:right-5">
          <ArrowDownIcon />
        </div>
      )}
    </div>
  );
};
