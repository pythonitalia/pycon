type Props = {
  autoComplete?: string;
  name: string;
  id: string;
  type: string;
  required?: boolean;
  label: string;
};

export const Input: React.FC<Props> = ({ label, id, ...props }) => (
  <div>
    <label htmlFor={id} className="block text-sm font-medium text-gray-700">
      {label}
    </label>

    <div className="mt-1">
      <input
        className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        id={id}
        {...props}
      />
    </div>
  </div>
);
