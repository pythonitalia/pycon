export enum Action {
  AUTH = "auth",
}

export abstract class PastaportoAction<Options, Return, Payload> {
  constructor(
    readonly payload: Payload,
    readonly options: Options | null = null,
  ) {}

  abstract apply(context: any): Promise<Return>;
}
