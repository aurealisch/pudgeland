using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class CommonApplicationCommandModule
    {
        partial class ShopApplicationCommandModule
        {
            [SlashCommand("покупка", "Покупка предмета из магазина")]
            public async Task PurchaseSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
