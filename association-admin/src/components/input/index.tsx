import classnames from "classnames";

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
};

export const Input: React.FC<Props> = ({
  label,
  id,
  errorMessage,
  icon: Icon,
  ...props
}) => (
  <div className="relative rounded-md shadow-sm">
    {label && (
      <label htmlFor={id} className="block text-sm font-medium text-gray-700">
        {label}
      </label>
    )}

    {Icon && (
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Icon className="mr-3 mt-1 h-4 w-4 text-gray-400 stroke-current" />
      </div>
    )}

    <div className="mt-1">
      <input
        className={classnames(
          "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
          {
            "border-red-500": !!errorMessage,
            "pl-9": !!Icon,
          },
        )}
        id={id}
        {...props}
      />
      {errorMessage && <div className="text-red-500">{errorMessage}</div>}
    </div>
  </div>
);
