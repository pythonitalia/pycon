import { ReactComponentElement } from "react";

type MenuItemProps = {
  title: string;
  description?: string;
  icon?: React.ElementType;
};

const MenuItem: React.FC<MenuItemProps> = ({ title, description, icon }) => {
  return (
    <a
      href="#"
      className="-m-3 p-3 flex items-start rounded-lg hover:bg-gray-50"
    >
      <div className="flex-shrink-0 flex items-center justify-center h-10 w-10 rounded-md bg-gradient-to-r from-purple-600 to-indigo-600 text-white sm:h-12 sm:w-12">
        {/* Heroicon name: outline/inbox */}
        {icon}
        <svg
          className="h-6 w-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
          />
        </svg>
      </div>
      <div className="ml-4">
        <p className="text-base font-medium text-gray-900">{title}</p>
        <p className="mt-1 text-sm text-gray-500">{description}</p>
      </div>
    </a>
  );
  //  mobile version
  //   return (
  //     <a
  //       href="#"
  //       className="-m-3 p-3 flex items-center rounded-lg hover:bg-gray-50"
  //     >
  //       <div className="flex-shrink-0 flex items-center justify-center h-10 w-10 rounded-md bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
  //         <svg
  //           className="h-6 w-6"
  //           xmlns="http://www.w3.org/2000/svg"
  //           fill="none"
  //           viewBox="0 0 24 24"
  //           stroke="currentColor"
  //           aria-hidden="true"
  //         >
  //           <path
  //             strokeLinecap="round"
  //             strokeLinejoin="round"
  //             strokeWidth={2}
  //             d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
  //           />
  //         </svg>
  //       </div>
  //       <div className="ml-4 text-base font-medium text-gray-900">
  //         Knowledge Base
  //       </div>
  //     </a>
  //   );
};
export default MenuItem;
