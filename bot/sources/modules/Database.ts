import { PrismaClient, type User } from "@prisma/client";
import { isNullish } from "@sapphire/utilities";
import log from "@utilities/log";

export default class Database {
  constructor(private prisma: PrismaClient) {}

  @log("Connecting to database")
  async connect(): Promise<void> {
    await this.prisma.$connect();
  }

  @log("Disconnecting to database")
  async disconnect(): Promise<void> {
    await this.prisma.$disconnect();
  }

  @log("Getting user")
  async getUser(id: string): Promise<User> {
    const user = await this.prisma.user.findUnique({
      where: {
        id,
      },
    });

    if (isNullish(user)) {
      return await this.prisma.user.create({
        data: {
          id,
        },
      });
    }

    return user;
  }

  @log("Updating user")
  async updateUser(options: {
    action: "increment" | "decrement";
    id: string;
    key: keyof User;
    value?: number;
  }) {
    await this.prisma.user.update({
      where: {
        id: options.id,
      },
      data: {
        [options.key]: {
          [options.action]: options.value || 1,
        },
      },
    });
  }

  @log("Setting minecraft display name")
  async setMinecraftDisplayName(options: { id: string; value: string }) {
    await this.prisma.user.update({
      where: {
        id: options.id,
      },
      data: {
        minecraftDisplayName: options.value,
      },
    });
  }
}
