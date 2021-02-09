import { FieldError } from "./types";

export const getMergedErrors = (errors: FieldError[]) =>
  (errors || []).map((error) => error.message).join(",");
