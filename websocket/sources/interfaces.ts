import { type ServerWebSocket } from "bun";
import { Code } from "./enums";

export interface Request {
  code: Code;
  data?: any;
}

export interface Options {
  ws: ServerWebSocket<unknown>;
  data?: any | undefined;
}
