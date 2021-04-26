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

export const Button: React.FC<ButtonProps> = ({
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
        <a href={link} target="_blank" rel="noopener noreferrer">
          {text}
        </a>
      )}
      {!link && <span>{text}</span>}
    </button>
  );
};
