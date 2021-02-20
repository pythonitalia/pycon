import classnames from "classnames";
import { ButtonHTMLAttributes, Fragment } from "react";

export enum ButtonVariant {
  DEFAULT = "default",
  PAGINATION = "pagination",
}

type Props = {
  block?: boolean;
  href?: string;
  type?: ButtonHTMLAttributes<HTMLButtonElement>["type"];
  className?: string;
  onClick?: () => void;
  variant?: ButtonVariant;
};

export const Button: React.FC<Props> = ({
  children,
  block = true,
  href,
  type = "submit",
  className,
  onClick,
  variant = ButtonVariant.DEFAULT,
}) => {
  const Wrapper = href ? "a" : Fragment;
  let wrapperProps;

  if (href) {
    wrapperProps = {
      href,
      target: "_blank",
    };
  }

  return (
    <Wrapper {...wrapperProps}>
      <button
        onClick={onClick}
        type={type}
        className={classnames(
          "flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
          {
            "w-full": block,
            "text-white bg-indigo-600 hover:bg-indigo-700":
              variant == ButtonVariant.DEFAULT,
            "text-gray-500 hover:bg-gray-50 text-sm font-medium border-gray-300 bg-white":
              variant == ButtonVariant.PAGINATION,
          },
          className,
        )}
      >
        {children}
      </button>
    </Wrapper>
  );
};
