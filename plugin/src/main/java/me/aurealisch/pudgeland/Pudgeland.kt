package me.aurealisch.pudgeland

import org.bukkit.plugin.java.JavaPlugin

class Pudgeland : JavaPlugin()
{
    override fun onEnable()
    {
        val drugs = mapOf<Drug, DrugItem>(
            Drug.SmokingPipe to DrugItem("Трубка для курения"),
            Drug.Syringe to DrugItem("Шприц"),
            Drug.TobaccoLeaf to DrugItem("Лист табака"),
            Drug.GooseberryLeaf to DrugItem("Лист крыжовника"),
            Drug.DriedTobaccoLeaf to DrugItem("Сушенный лист Табака"),
            Drug.DriedGooseberryLeaf to DrugItem("Сушенный лист Крыжовника"),
            Drug.DiamondCrystals to DrugItem("Кристаллы Алмаза"),
            Drug.SyringeWithCactus to DrugItem("Шприц с Кактусом"),
            Drug.RedGlowstonePowderSnuffMixture to DrugItem("Ред-глоустоуновая пороховая нюхательная смесь"),
            Drug.WeezerWheels to DrugItem("Визер колёса")
        )
    }

    override fun onDisable()
    {
        // Plugin shutdown logic
        logger.info("Goodbye, World!")
    }
}
