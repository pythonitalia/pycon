import classnames from "classnames";

type ModalProps = {
  showModal: boolean;
  closeModalHandler?: (e: React.MouseEvent | React.FormEvent) => void;
  className?: string;
};

export const Modal: React.FC<ModalProps> = ({
  showModal = true,
  closeModalHandler,
  children,
  className,
}) => (
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
        <div className="px-6">{children}</div>
      </div>
    </div>
  </div>
);
