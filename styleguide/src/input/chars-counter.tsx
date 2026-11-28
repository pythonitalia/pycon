import React from "react";
import { Text } from "../text";

type Props = {
  maxLength?: number;
  value: React.InputHTMLAttributes<HTMLInputElement>["value"];
};
export const CharsCounter = ({ maxLength, value }: Props) => {
  if (!maxLength) {
    return null;
  }

  const currentLength = String(value ?? "").length || 0;
  return (
    <Text size="label4">
      {currentLength}/{maxLength}
    </Text>
  );
};
