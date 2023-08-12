using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class ImagesApplicationCommandModule
    {
        partial class AnimalsApplicationCommandModule
        {
            [SlashCommand("кошка", "Случайное изображение кошки")]
            public async Task CatSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
