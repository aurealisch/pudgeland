declare module "bun" {
  interface Env {
    TOKEN: string;
    ADDRESS: string;
    PORT: number;
  }
}
