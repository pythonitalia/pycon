import Head from "next/head";
import React from "react";
import { useFormState } from "react-use-form-state";
import Button from "~/components/button/button";
import { Divider } from "~/components/divider/divider";
import LoginIcon from "~/components/icons/login";
import Input from "~/components/input/input";
import Link from "~/components/link/link";
import Logo from "~/components/logo/logo";

type LoginFormFields = {
  email: string;
  password: string;
};

const LoginPage = () => {
  const [formState, { email, password }] = useFormState<LoginFormFields>({});

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formState.values);
  };

  return (
    <>
      <Head>
        <title>Log in</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <Logo />
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Sign in to your account
            </h2>
          </div>
          <form
            className="mt-8 space-y-6"
            action="#"
            method="POST"
            onSubmit={handleSubmit}
          >
            <div className="rounded-md shadow-sm -space-y-px">
              <Input
                id={"email-address"}
                label={"Email address"}
                placeholder={"email@pycon.it"}
                {...email("email")}
                required
              />
              <Link text={"Don't have an account?"} to="/signup" />

              <Input
                id={"password"}
                label={"Password"}
                {...password("password")}
                required
                minLength={8}
              />
              <Link text={"Forgot your password?"} to="/forgot-password" />
            </div>

            <div>
              <Button>
                <span className="absolute left-0 inset-y-0 flex flex-row-reverse items-center pl-3">
                  <LoginIcon className="h-5 w-5 text-blue-100 group-hover:text-blue-400" />
                </span>
                Log in
              </Button>
            </div>
          </form>

          <Divider text={"Or continue with..."} />
        </div>
      </div>
    </>
  );
};

export default LoginPage;
