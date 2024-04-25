import { initTRPC } from '@trpc/server';
import type { Context } from './context';

export const { procedure, router } = initTRPC.context<Context>().create();
