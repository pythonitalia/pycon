import { useState } from "react";
import { Text, Textarea, TextareaProps } from "theme-ui";

type LimitedTextareaPros = TextareaProps & {
  limit: number;
};
const LimitedTextarea = ({
  value,
  limit,
  onChange,
  ...props
}: LimitedTextareaPros) => {
  const [content, setContent] = useState(value.slice(0, limit));

  return (
    <>
      <Textarea
        onChange={(event) => {
          onChange(event);
          setContent(event.target.value.slice(0, limit));
        }}
        value={value}
        {...props}
      />
      <Text
        variant="labelDescription"
        as="p"
        mb={4}
        color={value.length >= limit ? "red" : "black"}
      >
        {content.length}/{limit}
      </Text>
    </>
  );
};

export default LimitedTextarea;
