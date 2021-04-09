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
        <div className="relative max-w-sm w-full mx-auto bg-white overflow-hidden shadow-xl">
          <div
            className="py-3 bg-gray-100 cursor-pointer	"
            onClick={(e) => closeModalHandler?.(e)}
          >
            Chiudi
          </div>
          <div className="px-6">{children}</div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
