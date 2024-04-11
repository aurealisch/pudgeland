package me.aurealisch.pudgeland;

import me.aurealisch.pudgeland.commandExecutors.ConnectCommandExecutor;
import me.aurealisch.pudgeland.commandExecutors.DisconnectCommandExecutor;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.Objects;
import java.util.logging.Logger;

@SuppressWarnings("unused")
public final class Pudgeland extends JavaPlugin {
    Logger logger;
    WebSocketClientEndpoint webSocketClientEndpoint;

    @Override
    public void onEnable() {
        // Plugin startup logic
        this.logger = getLogger();
        this.webSocketClientEndpoint = new WebSocketClientEndpoint(this);

        logger.info("Hello, World!");

        Objects.requireNonNull(getCommand("connect")).setExecutor(new ConnectCommandExecutor(this));
        Objects.requireNonNull(getCommand("disconnect")).setExecutor(new DisconnectCommandExecutor(this));
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
        logger.info("Goodbye, World!");
    }
}
