import LoginIcon from "../icons/login";
import clsx from "clsx";
import React from "react";

type ButtonProps = {
  disabled?: boolean;
  loading?: boolean;
  type?: "button" | "reset" | "submit";
  className?: string;
  onClick?: () => void;
};

const Button: React.FC<ButtonProps> = ({
  type,
  className,
  children,
  ...props
}) => {
  return (
    <button
      type={type}
      className={clsx(
        "group relative w-full flex justify-center py-2 px-4",
        "border border-transparent",
        "text-sm font-medium rounded-md text-white",
        "bg-blue hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",

        className
      )}
    >
      <span className="absolute left-0 inset-y-0 flex flex-row-reverse items-center pl-3">
        <LoginIcon className="h-5 w-5 text-blue-100 group-hover:text-blue-400" />
      </span>
      {children}
    </button>
  );
};
export default Button;
