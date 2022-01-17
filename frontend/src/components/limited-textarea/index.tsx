import { useState } from "react";
import { Text, Textarea, TextareaProps } from "theme-ui";

export const LimitedTextarea = ({
  value,
  maxLength,
  ...props
}: TextareaProps) => {
  return (
    <>
      <Textarea value={value} maxLength={maxLength} {...props} />
      <Text
        variant="labelDescription"
        as="p"
        mb={4}
        color={(value as string)?.length >= maxLength ? "red" : "black"}
      >
        {(value as string)?.length}/{maxLength}
      </Text>
    </>
  );
};

