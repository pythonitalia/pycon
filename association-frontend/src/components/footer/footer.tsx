const Footer = () => {
  return (
    <footer className="bg-gray-50" aria-labelledby="footerHeading">
      <h2 id="footerHeading" className="sr-only">
        Footer
      </h2>

      <div className="max-w-4xl mx-auto px-4 lg:px-8 border-t border-gray-200">
        <div className="py-4 text-center ">
          <p className="text-gray-400 text-xs ">
            Python Italia with some rights reserved
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
