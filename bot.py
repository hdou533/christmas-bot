import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')

# Intents for bot permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)


reaction_role_mapping = {
    "🎅": "Santa",    
    "🦌": "Rudolph",   
    "⛄": "Snowman"
}

@bot.event
async def on_ready():
    print("Bot is ready!")

    # Print all available roles for the bot to see
    for role in bot.guilds[0].roles:
        print(f"Role: {role.name}")

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is in the right channel and made by a non-bot user
    if user.bot:
        return

    # Check if the reaction is on the correct message (you can store message ID when sending the role message)
    if reaction.message.id != message.id:  # `message` is the message object where you send the roles
        return

   

    # Check if the emoji is in the reaction role mapping
    if reaction.emoji in reaction_role_mapping:
        role_name = reaction_role_mapping[reaction.emoji]
        role = discord.utils.get(reaction.message.guild.roles, name=role_name)

        if role:
            # Assign the role to the user
            member = reaction.message.guild.get_member(user.id)

            # Remove all other Christmas-related roles
            for emoji, role_name in reaction_role_mapping.items():
                if emoji != reaction.emoji:
                    existing_role = discord.utils.get(reaction.message.guild.roles, name=role_name)
                    if existing_role in member.roles:
                        await member.remove_roles(existing_role)


            await member.add_roles(role)
            print(f"Assigned {role_name} role to {user.name}")

        else:
            print(f"Role {role_name} not found!")

@bot.event
async def on_reaction_remove(reaction, user):
    # Ignore bot reactions
    if user.bot:
        return

    # Check if the emoji is in the reaction-role mapping
    role_name = reaction_role_mapping.get(reaction.emoji)
    if role_name:
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            # Remove role from user
            await user.remove_roles(role)
            print(f"Removed {role_name} from {user.name}")

# Command to create the reaction role message
@bot.command(name='hohoho~')
async def hohoho(ctx):
    description = "\n".join([f"{emoji}: {role}" for emoji, role in reaction_role_mapping.items()])
    embed = discord.Embed(title="Choose Your Christmas Role!", description=description, color=0x00ff00)

    # Store the message ID so we can check it later
    global message  # This makes the message ID available for the on_reaction_add event
    # Send the embed message and get its ID
    message = await ctx.send(embed=embed)

    # Add reactions to the message
    for emoji in reaction_role_mapping.keys():
        await message.add_reaction(emoji)

    
    message = message


@bot.command()
async def snowflakes(ctx):
    # Link to an animated snowflake GIF
    snowflake_url = "https://www.freepik.com/free-vector/falling-white-snow-overlay-transparent-background-snowflakes-layer-snow-pattern-texture-vector_154657990.htm#fromView=keyword&page=1&position=0&uuid=d8cab38e-aa0b-4277-a9d7-f72d176df9cf&new_detail=true" 

    embed = discord.Embed(title="❄️ Snowflakes! ❄️", description="Watch the snowflakes fall!", color=discord.Color.blue())
    embed.set_image(url=snowflake_url)  

    await ctx.send(embed=embed)

@bot.command()
async def santa(ctx):
    # Link to an animated Santa GIF
    santa_url = "https://i.gifer.com/tGJ.gif" 

    embed = discord.Embed(title="🎅 Santa is here! 🎅", description="Ho Ho Ho!", color=discord.Color.red())
    embed.set_image(url=santa_url)  

    await ctx.send(embed=embed)


@bot.command(name="jingletips")
async def jingletips(ctx):
    embed = discord.Embed(
        title="🎄 Christmas Bot Commands 🎄",
        description="Here are the commands you can use to celebrate the holiday season with our bot!",
        color=discord.Color.green()
    )
    embed.add_field(
        name="🎅 `!hohoho~`",
        value="Create a Christmas role selection message where you can choose your festive role.",
        inline=False
    )
    embed.add_field(
        name="❄️ `!snowflakes`",
        value="Watch falling snowflakes in the channel.",
        inline=False
    )
    embed.add_field(
        name="🎅 `!santa`",
        value="Display a Santa GIF to spread some holiday cheer!",
        inline=False
    )
    embed.add_field(
        name="🎄 `!jingletips`",
        value="Get a list of available commands for the Christmas bot.",
        inline=False
    )
    await ctx.send(embed=embed)
    
    


# Run the bot
bot.run(TOKEN)
