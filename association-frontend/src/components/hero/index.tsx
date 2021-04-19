import { Logo } from "~/components/logo";

export const Hero = () => {
  return (
    <>
      <div className="relative h-screen bg-local bg-center bg-no-repeat bg-cover bg-pycon-group">
        {/* overlay */}
        <div className="absolute top-0 bottom-0 left-0 right-0 bg-black bg-opacity-40"></div>

        {/* header with logo */}
        <div className="absolute transform -translate-x-1/2 -translate-y-1/2 top-2/4 left-2/4">
          <div className="max-w-4xl m-auto">
            <div className="z-10 content-start top-3">
              <Logo className={"p-2 h-full w-52"} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
