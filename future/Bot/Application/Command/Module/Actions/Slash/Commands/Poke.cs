using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class ActionsApplicationCommandModule
    {
        [SlashCommand("тыкнуть", "Тыкнуть пользователя")]
        public async Task PokeSlashCommand(InteractionContext interactionContext)
        {
            await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
        }
    }
}
