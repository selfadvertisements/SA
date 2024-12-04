import discord
from datetime import datetime
from discord.ext import commands


from core import checks
from core.models import PermissionLevel

options_menu="You have provided invalid dept code.\n\n`mod` - Moderation Team\n`pt ` - Partnership Team\n`growth` - Growth Team\n`sales` - Sales Team\n`hr`- Human Resources\n`management` - Management\n"

DEPS_DATA = {
        "mod": {
        "category_id": 1300687208013103124 ,
        "pretty_name": "Moderation Team",
        "reminders": "When reporting a member, please make sure to provide valid proof.",
        "role_id": 1300688996929634386,
        "send_message_to_user": True
    },
        "pt": {
        "category_id": 1300687229399859220 ,
        "pretty_name": "Partnership Team",
        "reminders": "Please have your advertisement ready to send and ensure you meet our requirements.",
        "role_id": 1300688998099849297,
        "send_message_to_user": True
    },
        "growth": {
        "category_id": 1300687279622193182 ,
        "pretty_name": "Growth Team",
        "reminders": "None",
        "role_id": 1300689059164979271,
        "send_message_to_user": True
    },
        "sales": {
        "category_id": 1300687297754435684 ,
        "pretty_name": "Sales Team",
        "reminders": "None",
        "role_id": 1300689059924017162,
        "send_message_to_user": True
    },
        "hr": {
        "category_id": 1300687185426513972 ,
        "pretty_name": "Human Resources Team",
        "reminders": "If you're looking to report a staff member, please make sure to provide valid proof against this staff member.",
        "role_id": 1286882045380792350,
        "send_message_to_user": True
    },
        "management": {
        "category_id": 1300687105038618746 ,
        "pretty_name": "Management Team",
        "reminders": "None",
        "role_id": 1300688479297998848,
        "send_message_to_user": True
    },
}
class SA(commands.Cog, name="SA Main Commands"):
    def __init__(self, bot):
        self.bot = bot
        
        
       
    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def transfer(self, ctx, *, to: str=None):
        """Command that transfers thread to other departments."""
        if to is None:
            embed = discord.Embed(title=f"Department Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Department Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        if data["send_message_to_user"]:
            mes = "You are being transferred to the **`"
            mes += data["pretty_name"]
            mes += "`**.\n"
            mes += "Please remain __patient__ while we find a suitable staff member to assist in your request.\n\n"
            
            if data["reminders"] is not None:
                mes += "**__Reminders__**\n"
                mes += data["reminders"]

            msg = ctx.message
            msg.content = mes
            
            await ctx.thread.reply(msg, anonymous = False)
        
        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("<@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def stransfer(self, ctx, to: str=None):
        """Silently transfers thread"""
        if to is None:
            embed = discord.Embed(title=f"Silent Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Silent Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("Silent Transfer - <@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def id(self, ctx):
        await ctx.send(ctx.thread.id)

async def setup(bot):
    await bot.add_cog(SA(bot))
