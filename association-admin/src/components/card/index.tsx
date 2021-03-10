import classnames from "classnames";

type Props = {
  center?: boolean;
  heading?: React.ReactNode;
};

export const Card: React.FC<Props> = ({
  children,
  center = false,
  heading,
}) => (
  <div
    className={classnames("mt-8", {
      "sm:mx-auto sm:w-full sm:max-w-md": center,
    })}
  >
    <div className="bg-white shadow rounded-lg">
      {heading && (
        <div className="border-b-2 border-gray-100 py-4 px-10">{heading}</div>
      )}
      <div className="py-4 px-10">{children}</div>
    </div>
  </div>
);
