import interactions
from interactions import listen
from interactions.api.events import *
from pymongo import MongoClient
import csv

# Initialize the Discord bot
bot = interactions.Client(
    token="YOUR_DISCORD_TOKEN",
    intents=interactions.Intents.DEFAULT | interactions.Intents.ALL,
)

# Connect to MongoDB
clientmongo = MongoClient("YOUR_MONGODB_CONNECTION_STRING")
db = clientmongo.SniperUser
UserCollection = db.SniperUser
User = [[],[]]

# Event handler for bot startup
@listen(Startup)
async def on_start():
    print("Bot has finished loading.")
    await bot.change_presence(activity="Helping SniperAIO members")

# Slash command for data conversion
@interactions.slash_command(name="convert", description="Convert data from CSV to MongoDB")
async def convert_data(ctx: interactions.SlashContext):
    # Check if the command invoker is authorized
    if ctx.author_id != 752231663173369877:
        return await ctx.send("You are not authorized to use this command.")

    # Read data from CSV file
    with open(file="./TabellaUser.csv", mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            userid = row['Username-List:']
            point = row['Point-list:']
            profit = row['User-Profit:']
            query = {"UserId": userid}

            try:
                if UserCollection.count_documents(query) == 0:
                    user = {
                        "UserId": userid,
                        "Name": User[0][User[1].index(userid)],
                        "ServerId": "930557411952066670",
                        "LastUse": "10/07/2023",
                        "PointDailyCount": 0,
                        "PointTotalCount": float(point),
                        "UserProfit": float(profit),
                    }
                    UserCollection.insert_one(user)
                    print(f"UserID: {userid} added to the database.")
                else:
                    print(f"UserID: {userid} already exists in the database.")
            except:
                print(f"User {userid} left.")

    # Send a completion message
    embed = interactions.Embed(
        title="Mery CSV Converter",
        color=0xFF0000
    )
    embed.add_field(
        name="Done",
        value="Data conversion completed.",
        inline=False
    )
    embed.set_footer(
        text="SniperAIO - Mery",
        icon_url="https://media.discordapp.net/attachments/933679396932444170/933679491077767208/Logo-real-3d-effect.jpg?width=662&height=662"
    )
    await ctx.send(embeds=embed)

# Start the bot
bot.start()
