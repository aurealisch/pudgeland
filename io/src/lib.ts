export enum PudgelandCode {
  Connect,
  Ok,
  Cancel,
}

export interface PudgelandData {
  id: string;
}

export interface PudgelandContent {
  code: PudgelandCode;
  data: PudgelandData;
}
