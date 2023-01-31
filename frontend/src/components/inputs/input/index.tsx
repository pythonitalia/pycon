import { Input as BaseInput, InputProps as BaseInputProps } from "theme-ui";

import { CharsCounter } from "../chars-counter";

type Props = BaseInputProps & {
  value?: string;
};

export const Input = ({ maxLength, value, ref, ...props }: Props) => {
  return (
    <>
      <BaseInput value={value} maxLength={maxLength} {...props} />
      <CharsCounter maxLength={maxLength} length={value?.length ?? 0} />
    </>
  );
};
