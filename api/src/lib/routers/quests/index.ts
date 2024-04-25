import { router } from '../../trpc';

export default router({
  message: await import('./procedures/message'),
  messageReaction: await import('./procedures/messageReaction'),
});
