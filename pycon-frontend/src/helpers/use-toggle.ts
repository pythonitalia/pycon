import { useState } from "react";

export const useToggle = (
  defaultValue: boolean,
): [boolean, () => void, () => void, () => void] => {
  const [value, setValue] = useState(defaultValue);

  const toggle = () => {
    setValue(!value);
  };

  const close = () => {
    setValue(false);
  };

  const open = () => {
    setValue(true);
  };

  return [value, toggle, open, close];
};
