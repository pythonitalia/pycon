import { default as NextLink } from "next/link";

type LinkProps = {
  text: string;
  to: string;
  className?: string;
};

const Link: React.FC<LinkProps> = ({ text, to, className }) => {
  return (
    <div className="flex items-center justify-between ">
      <div className="text-base mt-1">
        <NextLink href={to}>
          <a className=" font-medium text-indigo-600 hover:text-indigo-500">
            {text}
          </a>
        </NextLink>
      </div>
    </div>
  );
};
export default Link;
