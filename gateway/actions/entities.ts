export enum Action {
  AUTH = "auth",
}

export abstract class PastaportoAction {
  constructor(readonly payload: { [key: string]: string }) {}

  abstract apply(context: any): Promise<void>;
}
