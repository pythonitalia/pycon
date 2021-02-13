import classnames from "classnames";

export enum Variant {
  Search,
  Input,
}

type Props = {
  autoComplete?: string;
  name: string;
  id: string;
  type: string;
  required?: boolean;
  label?: string;
  placeholder?: string;
  errorMessage?: string;
  icon?: React.ExoticComponent<{ className: string }>;
  className?: string;
  variant?: Variant;
};

export const Input: React.FC<Props> = ({
  label,
  id,
  errorMessage,
  icon: Icon,
  className,
  variant = Variant.Input,
  ...props
}) => (
  <div
    className={classnames("relative rounded-md shadow-sm", {
      "h-full": variant === Variant.Search,
    })}
  >
    {label && (
      <label
        htmlFor={id}
        className="block text-sm font-medium text-gray-700 mb-1"
      >
        {label}
      </label>
    )}

    {Icon && (
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Icon className="mr-3 h-4 w-4 text-gray-400 stroke-current" />
      </div>
    )}

    <div
      className={classnames({
        "h-full": variant === Variant.Search,
      })}
    >
      <input
        className={classnames(
          "appearance-none block w-full px-3 py-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 placeholder-gray-400 focus:outline-none  sm:text-sm",
          {
            "border-red-500": !!errorMessage,
            "pl-9": !!Icon,

            "border-none border-t-0 h-full": variant === Variant.Search,
            "border rounded-md border-gray-300": variant === Variant.Input,
          },
          className,
        )}
        id={id}
        {...props}
      />
      {errorMessage && <div className="text-red-500">{errorMessage}</div>}
    </div>
  </div>
);
