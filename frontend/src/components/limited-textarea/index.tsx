import { useState } from "react";
import { Text, Textarea, TextareaProps } from "theme-ui";

type LimitedTextareaPros = TextareaProps & {
  value: string;
  limit: number;
};

const LimitedTextarea = ({ value, limit, ...props }: LimitedTextareaPros) => {
  return (
    <>
      <Textarea value={value} {...props} />
      <Text
        variant="labelDescription"
        as="p"
        mb={4}
        color={value.length >= limit ? "red" : "black"}
      >
        {value.length}/{limit}
      </Text>
    </>
  );
};

