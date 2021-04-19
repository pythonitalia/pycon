import classnames from "classnames";

type DividerProps = {
  borderClassName?: string;
  textClassName?: string;
  text?: string;
};

export const Divider: React.FC<DividerProps> = ({
  borderClassName,
  textClassName,
  text,
}) => {
  return (
    <div className="relative">
      <div className="absolute inset-0 flex items-center">
        <div
          className={classnames(
            "w-full border-t border-gray-300",
            borderClassName,
          )}
        />
      </div>
      <div className="relative flex justify-center text-base">
        <span
          className={classnames("px-2 bg-white text-gray-500", textClassName)}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
