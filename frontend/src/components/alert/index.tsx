import clsx from "clsx";
import React from "react";

type Props = {
  variant: "alert" | "success" | "info";
};

export const Alert = ({
  variant,
  children,
  ...props
}: React.PropsWithChildren<Props>) => {
  return (
    <div className="block my-2">
      <div
        className={clsx(
          "relative inline-block px-8 py-8 border before:content-[''] before:absolute before:top-0 before:left-0 before:w-2.5 before:h-full",
          {
            "before:bg-red": variant === "alert",
            "before:bg-green": variant === "success",
            "before:bg-blue": variant === "info",
          },
        )}
        {...props}
      >
        {children}
      </div>
    </div>
  );
};
