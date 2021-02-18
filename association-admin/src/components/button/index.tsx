import classnames from "classnames";
import { ButtonHTMLAttributes, Fragment } from "react";

type Props = {
  block?: boolean;
  href?: string;
  type?: ButtonHTMLAttributes<HTMLButtonElement>["type"];
  className?: string;
};

export const Button: React.FC<Props> = ({
  children,
  block = true,
  href,
  type = "submit",
  className,
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
      {" "}
      <button
        type={type}
        className={classnames(
          "flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
          {
            "w-full": block,
          },
          className,
        )}
      >
        {children}
      </button>
    </Wrapper>
  );
};
