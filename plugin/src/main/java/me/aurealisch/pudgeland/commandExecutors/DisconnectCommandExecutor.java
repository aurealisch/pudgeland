package me.aurealisch.pudgeland.commandExecutors;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

public class DisconnectCommandExecutor implements CommandExecutor {
    @Override
    public boolean onCommand(@NotNull CommandSender commandSender, @NotNull Command command, @NotNull String label, String[] arguments) {
        String name = command.getName();

        if (name.equals("disconnect")) return false;

        if (!(commandSender instanceof Player)) return false;

        Player player = (Player) commandSender;

        player.sendMessage("Disconnect");

        return true;
    }
}
