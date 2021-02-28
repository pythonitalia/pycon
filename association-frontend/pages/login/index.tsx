import FacebookIcon from "../../components/icons/facebook";
import { useLoginMutation } from "./login.generated";
import Head from "next/head";
import React from "react";
import { useFormState } from "react-use-form-state";
import Button from "~/components/button/button";
import { Divider } from "~/components/divider/divider";
import GoogleIcon from "~/components/icons/google";
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

  const [{ fetching, data }, login] = useLoginMutation();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formState.values);

    const result = await login({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });
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
              <Button fullWidth={true}>
                <span className="absolute left-0 inset-y-0 flex flex-row-reverse items-center pl-3">
                  <LoginIcon className="h-5 w-5 text-blue-100 group-hover:text-blue-400" />
                </span>
                Log in
              </Button>
            </div>
          </form>

          <Divider text={"Or continue with..."} />
          <div className="grid grid-cols-3 gap-4">
            <div>
              {" "}
              <Button fullWidth={true}>
                <FacebookIcon />
              </Button>
            </div>
            <div>
              <Button fullWidth={true}>
                <GoogleIcon />
              </Button>
            </div>
            <div>
              <Button fullWidth={true}>
                <LoginIcon className="h-5 w-5 text-blue-100 group-hover:text-blue-400" />
                Facebook
              </Button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
