import classnames from "classnames";

type Props = {
  variant?: "success" | "warning";
  className?: string;
};

export const Pill: React.FC<Props> = ({
  children,
  variant = "success",
  className,
}) => (
  <span
    className={classnames(
      "ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full select-none",
      {
        "bg-green-100 text-green-800": variant === "success",
        "bg-red-100 text-red-800": variant === "warning",
      },
      className,
    )}
  >
    {children}
  </span>
);
