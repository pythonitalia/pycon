import { Input as BaseInput } from "@python-italia/pycon-styleguide";

import { CharsCounter } from "../chars-counter";

type Props = any;

export const Input = ({ maxLength, value, ref, ...props }: Props) => {
  return (
    <>
      <BaseInput value={value} maxLength={maxLength} {...props} />
      <CharsCounter maxLength={maxLength} length={value?.length ?? 0} />
    </>
  );
};
