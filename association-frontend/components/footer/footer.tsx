import FacebookIcon from "../icons/facebook";
import GitHubIcon from "../icons/github";
import InstagramIcon from "../icons/instagram";
import LinkedInIcon from "../icons/linkedin";
import MailIcon from "../icons/mail";
import TwitterIcon from "../icons/twitter";

const Footer = () => {
  return (
    <footer className="bg-gray-50" aria-labelledby="footerHeading">
      <h2 id="footerHeading" className="sr-only">
        Footer
      </h2>
      <div className="max-w-7xl mx-auto pt-16 pb-8 px-4 sm:px-6 lg:pt-24 lg:px-8">
        <div className="mt-12 border-t border-gray-200 pt-8 md:flex md:items-center md:justify-between lg:mt-16">
          <div className="flex space-x-6 md:order-2">
            <a
              href="https://www.facebook.com/pythonitalia/"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">Facebook</span>
              <FacebookIcon />
            </a>
            <a
              href="https://www.instagram.com/python.it/"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">Instagram</span>
              <InstagramIcon />
            </a>
            <a
              href="https://twitter.com/PythonItalia"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">Twitter</span>
              <TwitterIcon />
            </a>
            <a
              href="https://github.com/pythonitalia"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">GitHub</span>
              <GitHubIcon />
            </a>
            <a
              href="https://www.linkedin.com/company/pycon-italia"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">LinkedIn</span>
              <LinkedInIcon />
            </a>
            <a
              href="https://discord.gg/VgrU8EJ734"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">Discord</span>

              <svg
                className="h-6 w-6"
                fill="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path d="m3.58 21.196h14.259l-.681-2.205c.101.088 5.842 5.009 5.842 5.009v-21.525c-.068-1.338-1.22-2.475-2.648-2.475l-16.767.003c-1.427 0-2.585 1.139-2.585 2.477v16.24c0 1.411 1.156 2.476 2.58 2.476zm10.548-15.513-.033.012.012-.012zm-7.631 1.269c1.833-1.334 3.532-1.27 3.532-1.27l.137.135c-2.243.535-3.26 1.537-3.26 1.537.104-.022 4.633-2.635 10.121.066 0 0-1.019-.937-3.124-1.537l.186-.183c.291.001 1.831.055 3.479 1.26 0 0 1.844 3.15 1.844 7.02-.061-.074-1.144 1.666-3.931 1.726 0 0-.472-.534-.808-1 1.63-.468 2.24-1.404 2.24-1.404-3.173 1.998-5.954 1.686-9.281.336-.031 0-.045-.014-.061-.03v-.006c-.016-.015-.03-.03-.061-.03h-.06c-.204-.134-.34-.2-.34-.2s.609.936 2.174 1.404c-.411.469-.818 1.002-.818 1.002-2.786-.066-3.802-1.806-3.802-1.806 0-3.876 1.833-7.02 1.833-7.02z" />
                <path d="m14.308 12.771c.711 0 1.29-.6 1.29-1.34 0-.735-.576-1.335-1.29-1.335v.003c-.708 0-1.288.598-1.29 1.338 0 .734.579 1.334 1.29 1.334z" />
                <path d="m9.69 12.771c.711 0 1.29-.6 1.29-1.34 0-.735-.575-1.335-1.286-1.335l-.004.003c-.711 0-1.29.598-1.29 1.338 0 .734.579 1.334 1.29 1.334z" />
              </svg>
            </a>
            <a
              href="mailto:info@python.it"
              className="text-gray-400 hover:text-gray-500"
            >
              <span className="sr-only">info@python.it</span>
              <MailIcon />
            </a>
          </div>
          <p className="mt-8 text-base text-gray-400 md:mt-0 md:order-1">
            Python Italia
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
