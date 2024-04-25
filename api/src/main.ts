import { createHTTPServer } from '@trpc/server/adapters/standalone';
import { appRouter } from '.';
import { createContext } from './lib/context';

createHTTPServer({
  createContext,
  router: appRouter,
}).listen(8081);
