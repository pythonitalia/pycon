import classnames from "classnames";

type ModalProps = {
  showModal: boolean;
  closeModalHandler?: (e: React.MouseEvent | React.FormEvent) => void;
  className?: string;
};

const Modal: React.FC<ModalProps> = ({
  showModal = true,
  closeModalHandler,
  children,
  className,
}) => {
  return (
    <div
      className={classnames(
        "fixed z-10 inset-0 overflow-y-auto",
        { hidden: !showModal },
        className,
      )}
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div className="flex items-center justify-center min-h-screen px-4 text-center">
        <div
          className="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
          aria-hidden="true"
          onClick={(e) => closeModalHandler?.(e)}
        />
        <div className="px-6 py-7 relative max-w-md w-full mx-auto bg-white overflow-hidden shadow-xl">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
