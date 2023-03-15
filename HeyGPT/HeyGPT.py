import os
import openai
from redbot.core import commands, checks, Config

class HeyGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=16080501420211005, force_registration=True)
        default_global = {
            "openai_api_key": None,
            "engine": "text-davinci-002"
        }
        self.config.register_global(**default_global)
        self.engines = {
            1: "text-davinci-002",
            2: "text-curie-002",
            3: "text-babbage-002",
            4: "text-ada-002",
            5: "text-davinci-003"
        }

    @commands.command(name="heygpt")
    async def heygpt(self, ctx, *, message: str):
        """Send a message to the AI and get a response."""
        api_key = await self.config.openai_api_key()
        if not api_key:
            return await ctx.send("The OpenAI API key is not set. Please ask the bot owner to set it using the `!setgptapikey` command.")

        openai.api_key = api_key
        engine = await self.config.engine()

        prompt = f"{ctx.author.name}: {message}\nAI:"
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        reply = response.choices[0].text.strip()
        await ctx.send(f"{ctx.author.mention} {reply}")

    @commands.command(name="setgptapikey")
    @checks.is_owner()
    async def setgptapikey(self, ctx, *, api_key: str):
        """Set the OpenAI API key."""
        await self.config.openai_api_key.set(api_key)
        await ctx.send("The OpenAI API key has been set successfully.")

    @commands.command(name="listgptengines")
    async def listgptengines(self, ctx):
        """List the available GPT-3 engines."""
        engine_list = "\n".join([f"{num}: {engine}" for num, engine in self.engines.items()])
        await ctx.send(f"Available GPT-3 engines:\n{engine_list}")

    @commands.command(name="setgptengine")
    async def setgptengine(self, ctx, designator: int):
        """Set the GPT-3 engine to use."""
        if designator not in self.engines:
            await ctx.send("Invalid engine designator. Use `!listgptengines` to see available engines.")
            return

        engine = self.engines[designator]
        await self.config.engine.set(engine)
        await ctx.send(f"The GPT-3 engine has been set to {engine}.")

def setup(bot):
    bot.add_cog(HeyGPT(bot))
