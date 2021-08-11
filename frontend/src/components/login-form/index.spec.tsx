/* eslint-disable @typescript-eslint/no-empty-function */
import Router, { useRouter } from "next/router";
import { mocked } from "ts-jest/utils";

import {
  act,
  fireEvent,
  MockedProvider,
  render,
  screen,
  userEvent,
  wait,
} from "~/test-utils";
import { LoginDocument } from "~/types";

import { LOGIN_KEY } from "../profile/hooks";
import { LoginForm } from "./index";

afterEach(() => {
  jest.clearAllMocks();
});

jest.mock("next/router", () => ({
  push: jest.fn(),
  useRouter: jest.fn(() => ({
    prefetch: () => null,
    events: {
      on: () => {},
      off: () => {},
    },
    replace: jest.fn().mockResolvedValue(true),
    pathname: "",
    route: "",
    query: {},
  })),
}));

const MockedRouterPush = mocked(Router.push, true);
const MockedUseRouter = mocked(useRouter, true);

const createLoginMock = (
  data,
  input = {
    email: "email@email.it",
    password: "password",
  },
) => [
  {
    request: {
      query: LoginDocument,
      variables: {
        input,
      },
    },
    result: {
      data,
    },
  },
];

const VALID_LOGIN_MOCKS = createLoginMock({
  login: {
    __typename: "LoginSuccess",
  },
});

describe("Login form", () => {
  test("should render", () => {
    render(
      <MockedProvider>
        <LoginForm />
      </MockedProvider>,
    );

    expect(screen.getByText("Don't have an account?")).toBeInTheDocument();
    expect(
      screen.getByText("Password forgotten? Click here to reset it!"),
    ).toBeInTheDocument();

    expect(screen.getByText("Email")).toBeInTheDocument();
    expect(screen.getByText("Password")).toBeInTheDocument();
    expect(screen.getByText("Login 👉")).toBeInTheDocument();
  });

  describe("with correct credentials", () => {
    test("should login and redirect to profile", async () => {
      render(
        <MockedProvider mocks={VALID_LOGIN_MOCKS}>
          <LoginForm />
        </MockedProvider>,
      );

      userEvent.type(screen.getByTestId("email-input"), "email@email.it");
      userEvent.type(screen.getByTestId("password-input"), "password");

      await act(() => {
        userEvent.click(screen.getByRole("button", { name: "Login 👉" }));
        return wait(1);
      });

      expect(window.localStorage.getItem(LOGIN_KEY)).toBe("true");
      expect(MockedRouterPush).toHaveBeenCalledWith(
        "/[lang]/profile",
        "/en/profile",
      );
    });

    test("should redirect to next url if passed via code", async () => {
      render(
        <MockedProvider mocks={VALID_LOGIN_MOCKS}>
          <LoginForm next="https://pycon.it" />
        </MockedProvider>,
      );

      fireEvent.change(screen.getByTestId("email-input"), {
        target: { value: "email@email.it" },
      });

      fireEvent.change(screen.getByTestId("password-input"), {
        target: { value: "password" },
      });

      await act(() => {
        userEvent.click(screen.getByRole("button", { name: "Login 👉" }));
        return wait(1);
      });

      expect(MockedRouterPush).toHaveBeenCalledWith(
        "https://pycon.it",
        "https://pycon.it",
      );
    });

    test("should redirect to next url if present in url", async () => {
      MockedUseRouter.mockImplementation(() => ({
        query: {
          next: "http://next-url.pycon.it",
        },

        route: "",
        pathname: "",
        asPath: "",
        isLocaleDomain: false,
        basePath: "",
        push: jest.fn(),
        replace: jest.fn(),
        prefetch: jest.fn(),
        reload: jest.fn(),
        back: jest.fn(),
        beforePopState: jest.fn(),
        events: {
          on: jest.fn(),
          off: jest.fn(),
          emit: jest.fn(),
        },
        isFallback: false,
        isPreview: false,
        isReady: false,
      }));

      render(
        <MockedProvider mocks={VALID_LOGIN_MOCKS}>
          <LoginForm />
        </MockedProvider>,
      );

      userEvent.type(screen.getByTestId("email-input"), "email@email.it");
      userEvent.type(screen.getByTestId("password-input"), "password");

      await act(() => {
        userEvent.click(screen.getByRole("button", { name: "Login 👉" }));
        return wait(1);
      });

      expect(MockedRouterPush).toHaveBeenCalledWith(
        "http://next-url.pycon.it",
        "http://next-url.pycon.it",
      );
    });
  });

  describe("with incorrect credentials", () => {
    test("shows error with wrong email/password combo", async () => {
      render(
        <MockedProvider
          mocks={createLoginMock({
            login: {
              __typename: "WrongEmailOrPassword",
            },
          })}
        >
          <LoginForm />
        </MockedProvider>,
      );

      fireEvent.change(screen.getByTestId("email-input"), {
        target: { value: "email@email.it" },
      });

      fireEvent.change(screen.getByTestId("password-input"), {
        target: { value: "password" },
      });

      await act(() => {
        fireEvent.click(screen.getByText("Login 👉"));
        return wait(1);
      });

      expect(
        screen.getByText("Wrong username or password"),
      ).toBeInTheDocument();
    });

    test("shows error if email is not in valid format", async () => {
      render(
        <MockedProvider
          mocks={createLoginMock(
            {
              login: {
                __typename: "LoginValidationError",
                errors: {
                  __typename: "LoginErrors",
                  email: [
                    {
                      message: "value is not a valid email address",
                      type: "value_error.email",
                      __typename: "FieldError",
                    },
                  ],
                  password: null,
                },
              },
            },
            {
              email: "email@email",
              password: "password",
            },
          )}
        >
          <LoginForm />
        </MockedProvider>,
      );

      userEvent.type(screen.getByTestId("email-input"), "email@email");
      userEvent.type(screen.getByTestId("password-input"), "password");

      await act(() => {
        userEvent.click(screen.getByRole("button", { name: "Login 👉" }));
        return wait(1);
      });

      expect(
        screen.getByText("value is not a valid email address"),
      ).toBeInTheDocument();
    });
  });
});
