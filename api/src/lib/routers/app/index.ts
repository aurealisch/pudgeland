import { router } from '../../trpc';

export const appRouter = router({
  quests: await import('../quests'),
  users: await import('../users'),
  getProfile: await import('./procedures/getProfile'),
});

export type AppRouter = typeof appRouter;
