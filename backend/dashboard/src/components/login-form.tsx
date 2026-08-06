import { useState } from "react";
import type { FormEvent } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

const LOGIN_MUTATION = `
  mutation DashboardLogin($input: LoginInput!) {
    login(input: $input) {
      __typename
      ... on LoginSuccess {
        user {
          id
        }
      }
      ... on LoginErrors {
        errors {
          email
          password
        }
      }
      ... on WrongEmailOrPassword {
        message
      }
    }
  }
`;

type LoginErrors = {
  email: string[];
  password: string[];
  form: string[];
};

type LoginResponse = {
  data?: {
    login?:
      | { __typename: "LoginSuccess" }
      | {
          __typename: "LoginErrors";
          errors: { email: string[]; password: string[] };
        }
      | { __typename: "WrongEmailOrPassword"; message: string };
  };
  errors?: Array<{ message: string }>;
};

export function LoginForm({
  className,
  nextUrl,
  ...props
}: React.ComponentProps<"div"> & { nextUrl: string }) {
  const [errors, setErrors] = useState<LoginErrors>({
    email: [],
    password: [],
    form: [],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function logIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrors({ email: [], password: [], form: [] });
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);

    try {
      const response = await fetch("/graphql", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
          query: LOGIN_MUTATION,
          variables: {
            input: {
              email: formData.get("email"),
              password: formData.get("password"),
            },
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`Login request failed with status ${response.status}`);
      }

      const payload = (await response.json()) as LoginResponse;

      if (payload.errors?.length) {
        setErrors({
          email: [],
          password: [],
          form: payload.errors.map((error) => error.message),
        });
        return;
      }

      const result = payload.data?.login;

      if (result?.__typename === "LoginSuccess") {
        window.location.assign(nextUrl);
        return;
      }

      if (result?.__typename === "LoginErrors") {
        setErrors({ ...result.errors, form: [] });
        return;
      }

      if (result?.__typename === "WrongEmailOrPassword") {
        setErrors({
          email: [],
          password: ["The email or password is incorrect."],
          form: [],
        });
        return;
      }

      throw new Error("Login response did not contain a result");
    } catch {
      setErrors({
        email: [],
        password: [],
        form: ["We couldn't log you in. Please try again."],
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Welcome back</CardTitle>
          <CardDescription>
            Sign in with your email and password.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={logIn}>
            <FieldGroup>
              <Field data-invalid={errors.email.length > 0}>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  aria-describedby={
                    errors.email.length ? "email-error" : undefined
                  }
                  aria-invalid={errors.email.length > 0}
                  autoComplete="email"
                  disabled={isSubmitting}
                  id="email"
                  name="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                />
                <FieldError
                  errors={errors.email.map((message) => ({ message }))}
                  id="email-error"
                />
              </Field>
              <Field data-invalid={errors.password.length > 0}>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <a
                    href="/reset-password"
                    className="ml-auto text-sm underline-offset-4 hover:underline"
                  >
                    Forgot your password?
                  </a>
                </div>
                <Input
                  aria-describedby={
                    errors.password.length ? "password-error" : undefined
                  }
                  aria-invalid={errors.password.length > 0}
                  autoComplete="current-password"
                  disabled={isSubmitting}
                  id="password"
                  name="password"
                  type="password"
                  required
                />
                <FieldError
                  errors={errors.password.map((message) => ({ message }))}
                  id="password-error"
                />
              </Field>
              <Field>
                <Button disabled={isSubmitting} type="submit">
                  {isSubmitting ? "Logging in…" : "Login"}
                </Button>
                <FieldError
                  errors={errors.form.map((message) => ({ message }))}
                />
                <FieldDescription className="text-center">
                  Don&apos;t have an account? <a href="/signup">Sign up</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
      <FieldDescription className="px-6 text-center">
        By clicking continue, you agree to our{" "}
        <a href="/terms-of-service">Terms of Service</a> and{" "}
        <a href="/privacy-policy">Privacy Policy</a>.
      </FieldDescription>
    </div>
  );
}
