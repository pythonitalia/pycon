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

type Props = {
  className?: string;
  deadline: Date;
  snakeLookingAt?: "left" | "right";
};

export const SnakeCountdown = ({
  className,
  deadline,
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
                id="snakeCountdown.hours"
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
                id="snakeCountdown.minutes"
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
                id="snakeCountdown.days"
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
                id="snakeCountdown.hours"
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
    <div className={clsx("max-w-[350px] lg:max-w-[400px]", className)}>
      <SnakeHead
        className={clsx(snakeBaseClasses, {
          "ml-auto mr-4": snakeLookingAt === "left",
          "scale-x-[-1] ml-4": snakeLookingAt === "right",
        })}
      />
      <div className="grid grid-cols-2 bg-green border-3 border-black divide-x-3">
        {boxes.map(({ value, label }, i) => (
          <CountdownBox key={i} value={value} label={label} />
        ))}
      </div>
      <SnakeTail
        className={clsx(snakeBaseClasses, {
          "ml-4": snakeLookingAt === "left",
          "scale-x-[-1] ml-auto mr-4": snakeLookingAt === "right",
        })}
      />
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
    <div className="p-9 flex items-center justify-center flex-col gap-2 uppercase">
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
