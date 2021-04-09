import classnames from "classnames";
import React from "react";

type ButtonProps = {
  disabled?: boolean;
  text?: string;
  link?: string;
  type?: "button" | "reset" | "submit";
  fullWidth?: boolean;
  onClick?: (...args: any[]) => void;
};

const Button: React.FC<ButtonProps> = ({
  type,
  link,
  text,
  fullWidth,
  children,
  ...props
}) => {
  return (
    <button
      type={type}
      onClick={props.onClick}
      className={classnames(
        "px-6 py-4 border border-transparent text-base font-bold text-bluecyan uppercase tracking-widest bg-yellow  hover:bg-bluecyan hover:text-yellow shadow-solidblue hover:shadow-solidyellow",
        {
          "w-full": fullWidth,
        },
      )}
    >
      {link && (
        <a href="https://pycon.it/en" target="_blank">
          {text}
        </a>
      )}
      {!link && text && <span>{text}</span>}
    </button>
  );
};
export default Button;
