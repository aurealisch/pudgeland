import type { User } from "@prisma/client";

type UnknownUser = Exclude<keyof User, "id">;

export default interface Quest {
  roleId: string;
  taskType: UnknownUser;
  taskRequiredVal: number;
  reward: {
    coins: number;
  };
}
