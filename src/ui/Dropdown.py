import nextcord
from nextcord import Interaction


class Dropdown(nextcord.ui.Select):
    def __init__(self) -> None:
        selectOptions = [
            nextcord.SelectOption(label="Opcion 1", description="Esta es la opción 1"),
            nextcord.SelectOption(label="Opcion 2", description="Esta es la opción 2"),
        ]

        super().__init__(
            placeholder="Elige una opción",
            min_values=1,
            max_values=1,
            options=selectOptions,
        )

    async def callback(self, interaction: Interaction):
        if self.values[0] == "Opcion 1":
            return await interaction.response.send_message("La opción 1 es la mejor")
        await interaction.response.send_message("You chose {self.values[0]}")


class DropdownView(nextcord.ui.View):
    def __init__(
        self,
    ):
        super().__init__(timeout=None)
        self.add_item(Dropdown())


# Uso de dropdown
"""     @nextcord.slash_command(name="test")
    async def test(self, interaction: Interaction):
        view = DropdownView()
        await interaction.send("Choose something", view=view) """
