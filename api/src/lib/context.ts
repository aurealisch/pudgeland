import { PrismaClient } from '@prisma/client';
import QuestManager from './QuestManager';

export async function createContext() {
  const questManager = new QuestManager();

  const prisma = new PrismaClient();
  const prismaUser = prisma.user;

  await prisma.$connect();

  return {
    questManager,
    prismaUser,
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
