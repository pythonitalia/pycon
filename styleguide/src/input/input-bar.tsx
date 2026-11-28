import clsx from "clsx";
import React from "react";
import { Spacer } from "../spacer";
import { Text } from "../text";
import { CharsCounter } from "./chars-counter";

type Props = {
  errors: (string | React.ReactNode)[];
  maxLength?: number;
  value: React.InputHTMLAttributes<HTMLInputElement>["value"];
};

export const InputBar = ({ maxLength, value, errors }: Props) => {
  return (
    <>
      <Spacer size="xs" />
      <div
        className={clsx("grid break-all grid-cols-[1fr_auto]", {
          "gap-4": !!maxLength,
        })}
      >
        <div>
          <Text as="p" size="label4" color="error" uppercase>
            {errors.join(", ")}
          </Text>
        </div>

        <CharsCounter value={value} maxLength={maxLength} />
      </div>
    </>
  );
};
