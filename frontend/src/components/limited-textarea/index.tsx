import { Text, Textarea, TextareaProps } from "theme-ui";

export const LimitedTextarea = ({
  value,
  maxLength,
  ...props
}: {
  value: string;
  maxLength: number;
} & TextareaProps) => {
  return (
    <>
      <Textarea value={value} maxLength={maxLength} {...props} />
      <Text
        variant="labelDescription"
        as="p"
        mb={4}
        color={value.length >= maxLength ? "red" : "black"}
      >
        {value.length}/{maxLength}
      </Text>
    </>
  );
};
