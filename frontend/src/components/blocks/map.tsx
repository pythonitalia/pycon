import { CmsMap } from "~/types";

export const MapBlock = ({ link, image, ...props }: CmsMap) => {
  return (
    <div className="border-2 border-red-500 bg-red-700 h-full w-full">
      <a
        target="_blank"
        rel="noopener noreferrer"
        href={link}
        className="w-full h-96 block bg-center"
        style={{
          backgroundImage: `url('${image}')`,
        }}
        {...props}
      />
    </div>
  );
};
