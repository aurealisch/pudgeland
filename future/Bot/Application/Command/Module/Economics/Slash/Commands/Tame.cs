using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class EconomicsApplicationCommandModule
    {
        [SlashCommand("приручить", "Попробовать приручить обезьяну")]
        public async Task TameSlashCommand(InteractionContext interactionContext)
        {
            await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
        }
    }
}
