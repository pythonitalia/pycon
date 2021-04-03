import React from "react";

import Button from "../button/button";
import GoogleIcon from "../icons/google";
import Input from "../input/input";
import Modal from "../modal/modal";

type ModalSigningProps = {
  isHidden: boolean;
};

const ModalSigning: React.FC<ModalSigningProps> = ({ isHidden }) => {
  return (
    <Modal isHidden={isHidden}>
      <div className="items-center">
        <h3
          className="mb-6 text-3xl text-center font-extrabold leading-6 text-gray-900"
          id="modal-title"
        >
          Entra nella community di Python Italia!
        </h3>

        <div className=" flex flex-col max-w-sm mx-auto ">
          <div className="mb-4 flex flex-col">
            <div className="">
              <Input placeholder={"Email"} />
            </div>
            <div className="place-self-start">
              <a
                href="#"
                className="underline text-bluecyan hover:text-yellow "
              >
                Hai gia' un account?
              </a>
            </div>
          </div>

          <div className="mb-4 flex flex-col">
            <div className="">
              <Input placeholder={"Password"} type={"password"} />
            </div>
            <div className="place-self-start">
              <a
                href="#"
                className=" underline text-bluecyan hover:text-yellow"
              >
                Hai dimenticato la password?
              </a>
            </div>
          </div>

          <div className="">
            <Button link={"/login"} text={"Accedi"} />
          </div>
          {/* <div className="mb-4 relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">
                Or continue with
              </span>
            </div>
          </div>

          <button className="flex justify-center appearance-none rounded-none px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-bluecyan focus:z-10 sm:text-xl rounded-t-md rounded-b-md ">
            <div className="px-3 flex items-right">
              <GoogleIcon />
            </div>

            <div className="text-gray-900">
              <a href="#" className="select-none">
                Continua con google
              </a>
            </div>
          </button> */}
        </div>
      </div>
    </Modal>
  );
  return null;
};

export default ModalSigning;
