import { Action, Code, Confirmation, Status } from "@/enums";
import type { Options, Request } from "@/interfaces";
import { fetch } from "@sapphire/fetch";
import { isNullish } from "@sapphire/utilities";

async function onSendMessage(opts: Options) {
  const data: { userId: string } | undefined = opts.data;

  if (isNullish(data)) return;

  const response = await fetch<{
    status: string;
  }>(`${process.env.ADDRESS}/confirm?id=${data.userId}`);

  opts.ws.subscribe("action");

  switch (Number(response.status)) {
    case Status.Ok: {
      opts.ws.subscribe("confirmation");
      opts.ws.publish("action", String(Action.Ready));
    }
  }

  opts.ws.unsubscribe("action");
}

async function onConfirmationAccepted(opts: Options) {
  const data: { userId: string } | undefined = opts.data;

  if (isNullish(data)) return;

  const response = await fetch<{
    status: string;
  }>(`${process.env.ADDRESS}/link?id=${data.userId}`);

  switch (Number(response.status)) {
    case Status.Ok: {
      opts.ws.publish("confirmation", String(Confirmation.Accepted));
      opts.ws.unsubscribe("confirmation");
    }
  }
}

async function onConfirmationRejected(opts: Options) {
  opts.ws.publish("confirmation", String(Confirmation.Rejected));
  opts.ws.unsubscribe("confirmation");
}

const codes: Record<Code, (opts: Options) => Promise<void>> = {
  [Code.SendMessage]: onSendMessage,
  [Code.ConfirmationAccepted]: onConfirmationAccepted,
  [Code.ConfirmationRejected]: onConfirmationRejected,
};

const server = Bun.serve({
  hostname: "0.0.0.0",
  fetch(request, server) {
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
