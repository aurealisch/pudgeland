package me.elaresai.pudgeland

import org.bukkit.plugin.java.JavaPlugin

class Pudgeland : JavaPlugin() {
    override fun onEnable() {
        // Plugin startup logic
        logger.info("Hello, World!")
    }

    override fun onDisable() {
        // Plugin shutdown logic
    }
}
