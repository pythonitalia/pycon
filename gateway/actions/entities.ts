export enum Action {
  AUTH = "auth",
}

export abstract class PastaportoAction<TOptions> {
  constructor(
    readonly payload: { [key: string]: string },
    readonly options: TOptions | null = null,
  ) {}

  abstract apply(context: any): Promise<any>;
}
