type InputProps = {
  id?: string;
  disabled?: boolean;
  required?: boolean;
  label?: string;
  placeholder?: string;
  css?: string;
  minLength?: number;
};

const Input: React.FC<InputProps> = ({
  label,
  css,
  placeholder = "",
  ...props
}) => {
  console.log({ label, props });

  return (
    <div className="">
      {label && (
        <div className="mb-2 mt-5">
          <label htmlFor={props.id} className=" text-xl">
            {label}
          </label>
        </div>
      )}
      <input
        id={props.id}
        className={
          "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-xl rounded-t-md rounded-b-md "
        }
        placeholder={placeholder}
        {...props}
      />
    </div>
  );
};
export default Input;
