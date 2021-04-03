import { useRef, useState } from "react";
import classnames from "classnames";

type ModalProps = {
  isHidden: boolean;
};

const Modal: React.FC<ModalProps> = ({ isHidden = true, children }) => {
  console.log({ isHidden });
  const [hide, setHide] = useState(isHidden);

  return (
    <div
      className={classnames("fixed z-10 inset-0 overflow-y-auto ", {
        hidden: isHidden,
      })}
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
      onClick={(e) => setHide(!hide)}
    >
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* {/* */}
        {/* Background overlay, show/hide based on modal state. */}

        {/* Entering: "ease-out duration-300" */}
        {/* From: "opacity-0" */}
        {/* To: "opacity-100" */}
        {/* Leaving: "ease-in duration-200" */}
        {/* From: "opacity-100" */}
        {/* To: "opacity-0" */}

        <div
          className="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
          aria-hidden="true"
        />
        {/* This element is to trick the browser into centering the modal contents. */}
        <span
          className="hidden sm:inline-block sm:align-middle sm:h-screen"
          aria-hidden="true"
        >
          ​
        </span>
        {/*
Modal panel, show/hide based on modal state.

Entering: "ease-out duration-300"
  From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
  To: "opacity-100 translate-y-0 sm:scale-100"
Leaving: "ease-in duration-200"
  From: "opacity-100 translate-y-0 sm:scale-100"
  To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
    */}
        <div className="px-6 py-7 absolute top-2/4 left-2/4 transform -translate-x-1/2 -translate-y-1/2  w-4/5 max-w-2xl  mx-auto bg-white overflow-hidden shadow-xl ">
          <div className="bg-white">
            {children}
            {/* <div className="sm:flex sm:items-start">

              <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3
                  className="text-lg leading-6 font-medium text-gray-900"
                  id="modal-title"
                >
                  Deactivate account
                </h3>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">
                    Are you sure you want to deactivate your account? All of
                    your data will be permanently removed. This action cannot be
                    undone.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Deactivate
            </button>
            <button
              type="button"
              className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancel
            </button> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
