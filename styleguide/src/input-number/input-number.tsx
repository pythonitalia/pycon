import clsx from "clsx";
import { Heading } from "../heading";
import { Text } from "../text";
import React from "react";

type Props = {
  values: { value: number | string; label: string | React.ReactNode }[];
  value?: number | string | undefined;
  onClick?: (value: number | string) => void;
};

export const InputNumber = ({ values, value, onClick }: Props) => {
  const valuesById = Object.fromEntries(
    values.map((value) => [value.value, value.label])
  );

  return (
    <div className="relative inline-block input-number-wrapper">
      <div className=" flex flex-row gap-1 md:gap-6">
        {values.map((element) => (
          <div
            key={element.value}
            className={clsx(
              "flex items-center justify-center font-sans text-md  rounded-full border-3  hover:bg-green cursor-pointer border-black w-10 h-10 md:w-16 md:h-16  transition-colors outline-none  leading-3 ",
              "input-number",
              {
                "bg-green": value === element.value,
                "bg-white": value !== element.value,
              }
            )}
            onClick={() => onClick?.(element.value)}
          >
            <Heading size={3}>{element.value}</Heading>

            <div
              className={clsx(
                "absolute input-number-label -bottom-2 md:bottom-auto left-0  md:left-full w-full md:ml-8 ",
                {
                  "active-element block": element.value === value,
                  hidden: element.value !== value,
                }
              )}
            >
              <Text size="label2">{valuesById[element.value]}</Text>
            </div>
          </div>
        ))}
      </div>
      <div className="md:hidden invisible">
        <Text size="label2">Value</Text>
      </div>
    </div>
  );
};
