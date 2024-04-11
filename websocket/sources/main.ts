import { Code, Status } from "@/enums";
import type { Options, Request } from "@/interfaces";
import { fetch } from "@sapphire/fetch";
import { createClient } from "redis";

const client = await createClient({
  url: process.env.REDIS_URL,
});

await client.connect();

interface Data {
  userId: string;
}

async function onSendConfirmation(
  opts: Options<Data & { minecraftDisplayName: string }>
) {
  const data = opts.data;
  const userId = data.userId;

  await client.set(userId, data.minecraftDisplayName);

  const response = await fetch<{
    status: string;
  }>(`${process.env.API_URL}/sendConfirmation?id=${userId}`);

  switch (Number(response.status)) {
    case Status.Ok: {
      opts.ws.subscribe("confirmation");
    }
  }
}

async function onConfirmationAccepted(opts: Options<Data>) {
  const userId = opts.data.userId;

  const minecraftDisplayName = await client.get(userId);

  const response = await fetch<{
    status: string;
  }>(
    `${process.env.API_URL}/confirmationAccepted?id=${userId}?minecraftDisplayName=${minecraftDisplayName}`
  );

  switch (Number(response.status)) {
    case Status.Ok: {
      opts.ws.publish("confirmation", String(Code.ConfirmationAccepted));
      opts.ws.unsubscribe("confirmation");
    }
  }
}

async function onConfirmationCanceled(opts: Options<Data>) {
  await client.del(opts.data.userId);

  opts.ws.publish("confirmation", String(Code.ConfirmationCanceled));
  opts.ws.unsubscribe("confirmation");
}

const codes: Record<Code, (opts: Options<any>) => Promise<void>> = {
  [Code.SendConfirmation]: onSendConfirmation,
  [Code.ConfirmationAccepted]: onConfirmationAccepted,
  [Code.ConfirmationCanceled]: onConfirmationCanceled,
};

Bun.serve({
  hostname: "0.0.0.0",
  fetch(request, server) {
    if (server.upgrade(request)) {
      return undefined;
    }

    return new Response("Hello, World!");
  },
  websocket: {
    async message(ws, message) {
      const request: Request = JSON.parse(message as string);

      await codes[request.code]({
        ws,
        data: request.data,
      });
    },
  },
});
