import { router } from '../../trpc';

export default router({
  create: await import('./procedures/create'),
  delete: await import('./procedures/delete'),
});
