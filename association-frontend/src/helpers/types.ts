export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = {
  [K in keyof T]: T[K];
};
export type MakeOptional<T, K extends keyof T> = Omit<T, K> &
  { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> &
  { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  _Any: any;
};

export type Query = {
  __typename?: "Query";
  _service: _Service;
  me: User;
};

export type User = {
  __typename?: "User";
  id: Scalars["Int"];
  email: Scalars["String"];
  fullname: Scalars["String"];
  name: Scalars["String"];
};

export type Mutation = {
  __typename?: "Mutation";
  login: LoginResult;
  register: RegisterResult;
};

export type MutationLoginArgs = {
  input: LoginInput;
};

export type MutationRegisterArgs = {
  input: RegisterInput;
};

export type LoginResult =
  | LoginSuccess
  | WrongEmailOrPassword
  | LoginValidationError;

export type LoginSuccess = {
  __typename?: "LoginSuccess";
  user: User;
  token: Scalars["String"];
};

export type WrongEmailOrPassword = {
  __typename?: "WrongEmailOrPassword";
  message: Scalars["String"];
};

export type LoginValidationError = {
  __typename?: "LoginValidationError";
  errors: LoginErrors;
};

export type LoginErrors = {
  __typename?: "LoginErrors";
  email?: Maybe<Array<FieldError>>;
  password?: Maybe<Array<FieldError>>;
};

export type FieldError = {
  __typename?: "FieldError";
  message: Scalars["String"];
  type: Scalars["String"];
};

export type LoginInput = {
  email: Scalars["String"];
  password: Scalars["String"];
};

export type RegisterResult =
  | RegisterSuccess
  | EmailAlreadyUsed
  | RegisterValidationError;

export type RegisterSuccess = {
  __typename?: "RegisterSuccess";
  user: User;
  token: Scalars["String"];
};

export type EmailAlreadyUsed = {
  __typename?: "EmailAlreadyUsed";
  message: Scalars["String"];
};

export type RegisterValidationError = {
  __typename?: "RegisterValidationError";
  errors: RegisterErrors;
};

export type RegisterErrors = {
  __typename?: "RegisterErrors";
  email?: Maybe<Array<FieldError>>;
  password?: Maybe<Array<FieldError>>;
};

export type RegisterInput = {
  email: Scalars["String"];
  password: Scalars["String"];
};

export type _Service = {
  __typename?: "_Service";
  sdl: Scalars["String"];
};
