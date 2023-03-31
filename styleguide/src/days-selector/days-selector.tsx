import clsx from "clsx";
import React from "react";
import { Heading } from "../heading";
import { Container } from "../container";
import { Spacer } from "../spacer";
import { Text } from "../text";

type Day = {
  date: string;
  selected: boolean;
};

type Props = {
  days: Day[];
  language: string;
  onClick?: (date: string) => void;
  children?: React.ReactNode;
  center?: boolean;
};

export const DaysSelector = ({
  days,
  language,
  onClick,
  children,
  center = false,
}: Props) => {
  const numberAndDayFormatter = new Intl.DateTimeFormat(language, {
    day: "numeric",
    month: "long",
  });
  const weekDayFormatter = new Intl.DateTimeFormat(language, {
    weekday: "long",
  });

  return (
    <Container noPadding>
      <div className="flex flex-col lg:flex-row lg:items-center justify-between">
        <div
          className={clsx(
            "flex overflow-scroll overflow-y-hidden snap-x snap-mandatory overflow-x-auto w-full",
            {
              "lg:items-center lg:justify-center": center,
            }
          )}
        >
          {days.map(({ date, selected }) => {
            const parsedDate = new Date(date);
            return (
              <div
                onClick={() => onClick?.(date)}
                key={date}
                className={clsx(
                  "basis-36 md:basis-[190px] cursor-pointer border shrink-0 text-center select-none snap-center",
                  "py-2 px-7 md:py-4 md:px-10 mx-2 first:ml-4 last:mr-4 hover:bg-coral transition",
                  {
                    "bg-milk/20 border-black/20": !selected,
                    "bg-coral border-black": selected,
                  }
                )}
              >
                <Heading size={3}>
                  {numberAndDayFormatter.format(parsedDate)}
                </Heading>
                <Spacer size="thin" />
                <Text
                  weight="strong"
                  size="label3"
                  color="black"
                  className="opacity-40"
                  uppercase
                >
                  {weekDayFormatter.format(parsedDate)}
                </Text>
              </div>
            );
          })}
        </div>
        {children}
      </div>
    </Container>
  );
};
