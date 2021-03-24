import classnames from "classnames";
import React from "react";

type ButtonProps = {
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "reset" | "submit";
  fullWidth?: boolean;
  onClick?: () => void;
};

const Button: React.FC<ButtonProps> = ({
  type,
  children,
  fullWidth = false,
  ...props
}) => {
  return (
    <button
      type={type}
      // group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
      className={classnames(
        "bg-gradient-to-r",
        "border",
        "border-transparent",
        "flex",
        "focus:outline-none",
        "focus:ring-2",
        "focus:ring-indigo-500",
        "focus:ring-offset-2",
        "font-medium",
        "group",
        "from-purple-600",
        "hover:from-purple-700",
        "hover:to-indigo-700",
        "inline-flex",
        "items-center",
        "justify-center",
        // "ml-8",
        "px-4",
        "py-2",
        "rounded-md",
        "shadow-sm",
        "text-base",
        "text-white",
        "to-indigo-600",
        "whitespace-nowrap",
        {
          "w-full": fullWidth,
        },
      )}
      onClick={props.onClick}
    >
      {children}
    </button>
  );
};
export default Button;
