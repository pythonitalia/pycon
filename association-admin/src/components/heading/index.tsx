import classnames from "classnames";

type Props = {
  align?: "center" | "left";
  size?: "large" | "medium";
  subtitle?: string;
  className?: string;
};

export const Heading: React.FC<Props> = ({
  size = "large",
  align = "left",
  children,
  subtitle,
  className,
}) => (
  <>
    <h1
      className={classnames(
        `text-${align} font-bold text-gray-700`,
        {
          "text-2xl": size === "large",
          "text-lg": size === "medium",
        },
        className,
      )}
    >
      {children}
    </h1>
    {subtitle && (
      <span className="text-gray-500 text-sm -mt-1 block">{subtitle}</span>
    )}
  </>
);
