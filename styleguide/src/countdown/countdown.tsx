import React from "react";
import { Heading } from "../heading";
import { Text } from "../text";
import { SnakeTail, SnakeHead } from "../illustrations";
import clsx from "clsx";
import {
  differenceInMinutes,
  differenceInHours,
  differenceInDays,
} from "date-fns";
import { isBefore } from "date-fns";
import { FormattedMessage } from "react-intl";
import { Color } from "../types";
import { getBackgroundClasses } from "../colors-utils";

type Props = {
  className?: string;
  deadline: Date;
  showSnake?: boolean;
  snakeLookingAt?: "left" | "right";
  background?: Color;
};

export const Countdown = ({
  className,
  deadline,
  background = "green",
  showSnake = false,
  snakeLookingAt = "left",
}: Props) => {
  const { days, hours, minutes } = timeLeftUntil(deadline);
  const boxes =
    days === 0
      ? [
          {
            value: hours,
            label: (
              <FormattedMessage
                id="countdown.hours"
                defaultMessage="{value, plural, one {hour} other {hours}}"
                values={{
                  value: hours,
                }}
              />
            ),
          },
          {
            value: minutes,
            label: (
              <FormattedMessage
                id="countdown.minutes"
                defaultMessage="{value, plural, one {minute} other {minutes}}"
                values={{
                  value: minutes,
                }}
              />
            ),
          },
        ]
      : [
          {
            value: days,
            label: (
              <FormattedMessage
                id="countdown.days"
                defaultMessage="{value, plural, one {day} other {days}}"
                values={{
                  value: days,
                }}
              />
            ),
          },
          {
            value: hours,
            label: (
              <FormattedMessage
                id="countdown.hours"
                defaultMessage="{value, plural, one {hour} other {hours}}"
                values={{
                  value: hours,
                }}
              />
            ),
          },
        ];

  const snakeBaseClasses = "w-24 lg:h-60 lg:w-52";

  return (
    <div className={clsx("max-w-[350px] lg:max-w-[410px]", className)}>
      {showSnake && (
        <SnakeHead
          className={clsx(snakeBaseClasses, {
            "ml-auto mr-4": snakeLookingAt === "left",
            "scale-x-[-1] ml-4": snakeLookingAt === "right",
          })}
        />
      )}
      <div
        className={clsx("grid grid-cols-2 border-3 border-black divide-x-3", {
          ...getBackgroundClasses(background),
        })}
      >
        {boxes.map(({ value, label }, i) => (
          <CountdownBox key={i} value={value} label={label} />
        ))}
      </div>
      {showSnake && (
        <SnakeTail
          className={clsx(snakeBaseClasses, {
            "ml-4": snakeLookingAt === "left",
            "scale-x-[-1] ml-auto mr-4": snakeLookingAt === "right",
          })}
        />
      )}
    </div>
  );
};

const CountdownBox = ({
  value,
  label,
}: {
  value: number;
  label: React.ReactNode;
}) => {
  return (
    <div className="py-9 px-14 flex items-center justify-center flex-col gap-2 uppercase">
      <Heading size="display2">{String(value).padStart(2, "0")}</Heading>
      <Text size="label2" weight="strong">
        {label}
      </Text>
    </div>
  );
};

const timeLeftUntil = (
  datetime: Date
): {
  days: number;
  hours: number;
  minutes: number;
} => {
  const now = new Date();

  if (isBefore(datetime, now)) {
    return { days: 0, hours: 0, minutes: 0 };
  }

  const days = differenceInDays(datetime, now);
  const hours = differenceInHours(datetime, now) - days * 24;
  const minutes =
    differenceInMinutes(datetime, now) - days * 24 * 60 - hours * 60;
  return { days, hours, minutes };
};
