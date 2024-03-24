import { Text } from "@python-italia/pycon-styleguide";
import clsx from "clsx";
import React from "react";

export const ErrorsList = ({
  errors,
  className,
}: {
  errors?: (string | React.ReactNode)[];
  className?: string;
}) => {
  if (!errors || errors.length === 0) {
    return null;
  }

  return (
    <ul className={clsx("text-red list-none pl-0", className)}>
      {errors
        .filter((error) => !!error)
        .map((error, index) => (
          <li key={index} className="pl-0">
            <Text size="label3" color="red">
              {error}
            </Text>
          </li>
        ))}
    </ul>
  );
};
