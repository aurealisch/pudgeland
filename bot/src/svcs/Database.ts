import { PrismaClient, type User } from "@prisma/client";
import { isNullish } from "@sapphire/utilities";

export default class Database {
  constructor(private prisma: PrismaClient) {}

  public async connect(): Promise<void> {
    return await this.prisma.$connect();
  }

  public async disconnect(): Promise<void> {
    return await this.prisma.$disconnect();
  }

  public async findUniqueUser(id: string): Promise<User | null> {
    return await this.prisma.user.findUnique({
      where: {
        id,
      },
    });
  }

  public async createUser(id: string): Promise<User> {
    return await this.prisma.user.create({
      data: {
        id,
      },
    });
  }

  public async findUniqueUserOrCreate(id: string): Promise<User> {
    const user = await this.findUniqueUser(id);

    if (isNullish(user)) {
      return await this.createUser(id);
    }

    return user;
  }

  public async increment(opts: {
    id: string;
    key: keyof User;
    val?: number;
  }): Promise<void> {
    await this.prisma.user.update({
      where: {
        id: opts.id,
      },
      data: {
        [opts.key]: {
          increment: opts.val || 1,
        },
      },
    });
  }

  public async decrement(opts: {
    id: string;
    key: keyof User;
    val?: number;
  }): Promise<void> {
    await this.prisma.user.update({
      where: {
        id: opts.id,
      },
      data: {
        [opts.key]: {
          decrement: opts.val || 1,
        },
      },
    });
  }
}
