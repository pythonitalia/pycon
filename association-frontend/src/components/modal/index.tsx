import classnames from "classnames";

type ModalProps = {
  showModal: boolean;
  closeModalHandler?: (e: React.MouseEvent | React.FormEvent) => void;
  className?: string;
  title: string;
};

export const Modal = ({
  showModal = true,
  closeModalHandler,
  children,
  className,
  title,
}: React.PropsWithChildren<ModalProps>) => (
  <div
    className={classnames(
      "fixed z-20 inset-0 overflow-y-auto",
      { hidden: !showModal },
      className,
    )}
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div className="flex items-center justify-center min-h-screen px-4 text-center">
      <div
        className="fixed inset-0 transition-opacity bg-gray-900 bg-opacity-75"
        aria-hidden="true"
        onClick={(e) => closeModalHandler?.(e)}
      />
      <div className="relative w-full max-w-sm mx-auto overflow-hidden bg-white shadow-xl">
        <div
          className="py-3 bg-gray-100 cursor-pointer "
          onClick={(e) => closeModalHandler?.(e)}
        >
          Chiudi
        </div>
        <div className="p-6">
          <h3
            className="mb-6 text-3xl font-extrabold text-center text-gray-900"
            id="modal-title"
          >
            {title}
          </h3>

          {children}
        </div>
      </div>
    </div>
  </div>
);
