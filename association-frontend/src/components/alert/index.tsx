import classnames from "classnames";

export enum Variant {
  INFO,
  ERROR,
}

type Props = {
  variant: Variant;
};

export const Alert = ({
  children,
  variant,
}: React.PropsWithChildren<Props>) => {
  return (
    <div
      className={classnames("text-left p-3 my-3 text-md", {
        "bg-blue-100": variant === Variant.INFO,
        "bg-red-200": variant === Variant.ERROR,
      })}
    >
      {children}
    </div>
  );
};
