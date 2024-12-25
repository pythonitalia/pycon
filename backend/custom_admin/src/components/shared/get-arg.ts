const CACHED_ARGS: Record<string, any> = {};

export const getArg = (arg: string) => {
  if (!CACHED_ARGS[arg]) {
    const tag = document.querySelector(`#arg-${arg}`);
    CACHED_ARGS[arg] = JSON.parse(tag?.innerHTML);
  }

  return CACHED_ARGS[arg];
};
