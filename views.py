import discord
from consts import *
from settings import *
from utility import *
from character import *

command_description = DESCRIPTION[COMMAND_LANGUAGE]

#SettingsView

class SettingsView(discord.ui.View):
    __s = Settings()
    def create(self, s:Settings):
        self.__s = s
    async def on_timeout(self):
        await self.message.edit(self.__s.d("timeout"), view=None)
    @discord.ui.select(
        placeholder = command_description["language"],
        min_values = 1,
        max_values = 1,
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="English",
                description="Use English",
                value="en"
            ),
            discord.SelectOption(
                label="中文",
                description="用中文",
                value="cn"
            )
        ]
    )
    async def language(self, select, interaction):
        self.__s.language = select.values[0]
        self.__s.updateSettings()
        await interaction.response.send_message(f"{self.__s.d('language response')}", ephemeral=True)

    @discord.ui.select(
        placeholder = command_description["color"],
        min_values = 1,
        max_values = 1,
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label=command_description["red"],
                description="",
                value="0"
            ),
            discord.SelectOption(
                label=command_description["orange"],
                description="",
                value="0.075"
            ),
            discord.SelectOption(
                label=command_description["yellow"],
                description="",
                value="0.15"
            ),
            discord.SelectOption(
                label=command_description["green"],
                description="",
                value="0.35"
            ),
            discord.SelectOption(
                label=command_description["aqua"],
                description="",
                value="0.5"
            ),
            discord.SelectOption(
                label=command_description["blue"],
                description="",
                value="0.675"
            ),
            discord.SelectOption(
                label=command_description["violet"],
                description="",
                value="0.75"
            ),
            discord.SelectOption(
                label=command_description["pink"],
                description="",
                value="0.875"
            )
        ]
    )
    async def color(self, select, interaction):
        self.__s.h = float(select.values[0])
        self.__s.updateSettings()
        await interaction.response.send_message(f"{self.__s.d('color response')}", ephemeral=True)

#ArtifactView

class ArtifactView(discord.ui.View):
    __s = Settings()
    def create(self, c:Character, s:Settings, ctx):
        self.__c = c
        self.__s = s
        self.__ctx = ctx
        self.__values = [-1,-1,-1]
    async def on_timeout(self):
        await self.message.edit(self.__s.d("timeout"), view=None)
    @discord.ui.select(
        placeholder =command_description["sands"],
        min_values = 1,
        max_values = 1,
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label=command_description["hp"],
                description="46.6%",
                value="0"
            ),
            discord.SelectOption(
                label=command_description["atk"],
                description="46.6%",
                value="1"
            ),
            discord.SelectOption(
                label=command_description["def"],
                description="46.6%",
                value="2"
            ),
            discord.SelectOption(
                label=command_description["em"],
                description="187",
                value="3"
            ),
            discord.SelectOption(
                label=command_description["er"],
                description="51.8%",
                value="6"
            )
        ]
    )
    async def sands(self, select, interaction):
        self.__values[0] = int(select.values[0])
        stats = [0,0,0,0,0,0,0,0,0]
        for v in self.__values:
            if (v == -1):
                pass
            elif (v >= 0):
                stats[v] += 1
            else:
                stats[abs(v)] = -1
        self.__c.main(stats)
        embed, image = embedCharacter(self.__c, self.__s, self.__ctx)
        await self.message.edit("", embed=embed, file=image)
        msg = self.__s.d("received") + self.__s.d("sands")
        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.select(
        placeholder =command_description["goblet"],
        min_values = 1,
        max_values = 1,
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label=command_description["hp"],
                description="46.6%",
                value="0"
            ),
            discord.SelectOption(
                label=command_description["atk"],
                description="46.6%",
                value="1"
            ),
            discord.SelectOption(
                label=command_description["def"],
                description="46.6%",
                value="2"
            ),
            discord.SelectOption(
                label=command_description["em"],
                description="187",
                value="3"
            ),
            discord.SelectOption(
                label=command_description["ele"],
                description="46.6%",
                value="7"
            ),
            discord.SelectOption(
                label=command_description["phys"],
                description="58.3%",
                value="-7"
            )
        ]
    )
    async def goblets(self, select, interaction):
        self.__values[1] = int(select.values[0])
        stats = [0,0,0,0,0,0,0,0,0]
        for v in self.__values:
            if (v == -1):
                pass
            elif (v >= 0):
                stats[v] += 1
            else:
                stats[abs(v)] = -1
        self.__c.main(stats)
        embed, image = embedCharacter(self.__c, self.__s, self.__ctx)
        await self.message.edit("", embed=embed, file=image)
        msg = self.__s.d("received") + self.__s.d("goblet")
        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.select(
        placeholder =command_description["hat"],
        min_values = 1,
        max_values = 1,
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label=command_description["hp"],
                description="46.6%",
                value="0"
            ),
            discord.SelectOption(
                label=command_description["atk"],
                description="46.6%",
                value="1"
            ),
            discord.SelectOption(
                label=command_description["def"],
                description="46.6%",
                value="2"
            ),
            discord.SelectOption(
                label=command_description["em"],
                description="187",
                value="3"
            ),
            discord.SelectOption(
                label=command_description["crate"],
                description="31.1%",
                value="4"
            ),
            discord.SelectOption(
                label=command_description["cdmg"],
                description="62.2%",
                value="5"
            ),
            discord.SelectOption(
                label=command_description["heal"],
                description="35.9%",
                value="8"
            )
        ]
    )
    async def hats(self, select, interaction):
        self.__values[2] = int(select.values[0])
        stats = [0,0,0,0,0,0,0,0,0]
        for v in self.__values:
            if (v == -1):
                pass
            elif (v >= 0):
                stats[v] += 1
            else:
                stats[abs(v)] = -1
        self.__c.main(stats)
        embed, image = embedCharacter(self.__c, self.__s, self.__ctx)
        await self.message.edit("", embed=embed, file=image)
        msg = self.__s.d("received") + self.__s.d("hat")
        await interaction.response.send_message(msg, ephemeral=True)