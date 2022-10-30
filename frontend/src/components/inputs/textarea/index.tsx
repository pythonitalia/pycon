import {
  Textarea as BaseTextarea,
  TextareaProps as BaseTextareaProps,
} from "theme-ui";

import { CharsCounter } from "../chars-counter";

type Props = BaseTextareaProps & {
  value?: string;
  cursor?: string;
};

export const Textarea = ({
  value,
  maxLength,
  ref,
  rows,
  cursor,
  ...props
}: Props) => {
  return (
    <>
      <BaseTextarea
        sx={{
          minHeight: 45 * rows,
          resize: "vertical",
          cursor,
        }}
        value={value}
        maxLength={maxLength}
        rows={rows}
        {...props}
      />
      <CharsCounter maxLength={maxLength} length={value!.length} />
    </>
  );
};
