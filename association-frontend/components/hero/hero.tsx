const Hero = () => {
  return (
    <header
      id="up"
      className="bg-center bg-fixed bg-no-repeat bg-center bg-cover relative"
    >
      {/* Overlay Background + Center Control */}
      <div
        className="content h-auto bg-opacity-50 bg-black flex items-center justify-center"
        style={{ background: "rgba(0,0,0,0.5)" }}
      >
        <div className="mx-2 text-center"></div>
      </div>
    </header>
  );
};
export default Hero;
