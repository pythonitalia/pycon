type InputProps = {
  id?: string;
  disabled?: boolean;
  required?: boolean;
  label?: string;
  placeholder?: string;
  css?: string;
  minLength?: number;
};

export const Input = ({
  label,
  css,
  placeholder = "",
  ...props
}: InputProps) => (
  <div>
    {label && (
      <div className="mt-5 mb-2">
        <label htmlFor={props.id} className="text-xl">
          {label}
        </label>
      </div>
    )}
    <input
      id={props.id}
      className={
        "appearance-none relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-bluecyan focus:z-10 sm:text-l"
      }
      placeholder={placeholder}
      {...props}
    />
  </div>
);
