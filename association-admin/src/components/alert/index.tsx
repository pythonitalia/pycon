import { ExclamationCircle } from "heroicons-react";

export const Alert: React.FC = ({ children }) => (
  <div className="rounded-md bg-red-50 p-4">
    <div className="flex">
      <div className="flex-shrink-0">
        <ExclamationCircle size={20} className="fill-current text-red-800" />
      </div>
      <div className="ml-3">
        <h3 className="text-sm font-medium text-red-800">{children}</h3>
      </div>
    </div>
  </div>
);
