from dataclasses import dataclass as dataclasses_dataclass


@dataclasses_dataclass
class Configuration:
    collecting_range_start: int
    collecting_range_stop: int
    domestication_base_cost: int
    domestication_multiplier: int
    purchase_coin_multiplier: int
    purchase_diamond_multiplier: int
    purchase_netherite_multiplier: int
