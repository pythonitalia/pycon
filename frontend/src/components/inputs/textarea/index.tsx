import {
  Textarea as BaseTextarea,
  TextareaProps as BaseTextareaProps,
} from "theme-ui";
import { CharsCounter } from "../chars-counter";

type Props = BaseTextareaProps & {
  value?: string;
};

export const Textarea = ({ value, maxLength, ref, ...props }: Props) => {
  return (
    <>
      <BaseTextarea value={value} maxLength={maxLength} {...props} />
      <CharsCounter maxLength={maxLength} length={value!.length} />
    </>
  );
};
