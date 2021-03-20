export enum Action {
  AUTH = "auth",
}

export abstract class PastaportoAction<Options, Return> {
  constructor(
    readonly payload: { [key: string]: string },
    readonly options: Options | null = null,
  ) {}

  abstract apply(context: any): Promise<Return>;
}
