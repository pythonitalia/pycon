import clsx from "clsx";
import React from "react";
import { InputBar } from "../input/input-bar";

type Props = React.TextareaHTMLAttributes<HTMLTextAreaElement> & {
  errors?: (string | React.ReactNode)[];
};

export const Textarea = ({ errors, ...props }: Props) => {
  const errorsOrEmpty = (errors ?? []).filter((e) => !!e);
  const hasError = errorsOrEmpty.length > 0;

  return (
    <div>
      <textarea
        {...props}
        className={clsx(
          "w-full font-sans text-md bg-transparent placeholder:text-grey-250 placeholder:font-sans border-b pb-2 transition-colors",
          "outline-none focus:border-green font-medium leading-3",
          {
            "border-red": hasError,
            "border-black": !hasError,
          }
        )}
        style={{
          minHeight: 45 * (props.rows ?? 1),
          resize: "vertical",
        }}
      />
      <InputBar
        value={props.value}
        maxLength={props.maxLength}
        errors={errorsOrEmpty}
      />
    </div>
  );
};
