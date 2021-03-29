import Logo from "~/components/logo/logo";

const Hero = () => {
  return (
    <>
      <div className="relative bg-cover bg-center bg-local bg-pycon-group bg-no-repeat h-screen">
        {/* overlay */}
        <div className="absolute top-0 left-0 bottom-0 right-0 bg-black bg-opacity-40"></div>

        {/* header with logo */}
        <div className="absolute top-2/4 left-2/4 transform -translate-x-1/2 -translate-y-1/2">
          <div className="max-w-4xl m-auto">
            <div className="content-start z-10 top-3">
              <Logo className={"p-2 h-full w-52"} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default Hero;
