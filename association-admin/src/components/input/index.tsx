import classnames from "classnames";

type Props = {
  autoComplete?: string;
  name: string;
  id: string;
  type: string;
  required?: boolean;
  label: string;
  errorMessage?: string;
};

export const Input: React.FC<Props> = ({
  label,
  id,
  errorMessage,
  ...props
}) => (
  <div>
    <label htmlFor={id} className="block text-sm font-medium text-gray-700">
      {label}
    </label>

    <div className="mt-1">
      <input
        className={classnames(
          "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
          {
            "border-red-500": !!errorMessage,
          },
        )}
        id={id}
        {...props}
      />
      {errorMessage && <div className="text-red-500">{errorMessage}</div>}
    </div>
  </div>
);
