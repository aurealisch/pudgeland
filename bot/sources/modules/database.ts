import { PrismaClient, User } from "@prisma/client";

export class Database {
  public constructor(private readonly prismaClient: PrismaClient) {}

  public async getUser(id: string): Promise<User> {
    let user = await this.prismaClient.user.findFirst({
      where: { id },
    });

    if (user != null) return user;

    return await this.prismaClient.user.create({
      data: { id },
    });
  }

  public async updateUser({
    id,
    ...data
  }: { id: string } & Partial<User>): Promise<User> {
    return await this.prismaClient.user.update({
      data,
      where: { id },
    });
  }
}
