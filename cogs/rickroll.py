import json
import os
import shutil
import random
import string
import sys

import discord
from discord.ext import commands
from PIL import Image
import requests

if not os.path.isfile("config.json"):
    sys.exit("config.json not found!")
else:
    with open("config.json") as file:
        config = json.load(file)


#constants
pfpSize = 128, 128
framesDir = config["root_dir"] + "assets/rickroll/"
soundFile = config["root_dir"] + "assets/rickroll/rickroll.mp3"
mapping = [[320, 180, 0],
 [320, 180, 0],
 [158, 72, 151],
 [320, 180, 0],
 [320, 180, 0],
 [158, 72, 149],
 [159, 67, 145],
 [320, 180, 0],
 [180, 82, 103],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [217, 129, 74],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [183, 88, 101],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [187, 94, 98],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [320, 180, 0],
 [178, 65, 110],
 [320, 180, 0],
 [320, 180, 0],
 [189, 99, 93],
 [144, 73, 150],
 [149, 72, 149],
 [220, 129, 74],
 [150, 70, 141],
 [164, 64, 38],
 [144, 62, 128],
 [122, 74, 81],
 [161, 48, 31],
 [160, 45, 31],
 [158, 44, 32],
 [320, 180, 0],
 [193, 104, 91],
 [320, 180, 0],
 [222, 129, 78],
 [145, 58, 120],
 [320, 180, 0],
 [128, 86, 81],
 [320, 180, 0],
 [147, 67, 127],
 [150, 66, 145],
 [138, 65, 35],
 [141, 64, 29],
 [150, 74, 155],
 [199, 110, 86],
 [223, 131, 78],
 [155, 79, 147],
 [157, 101, 31],
 [155, 64, 32],
 [320, 180, 0],
 [162, 53, 31],
 [320, 180, 0],
 [165, 45, 32],
 [320, 180, 0],
 [167, 39, 33],
 [320, 180, 0],
 [226, 137, 78],
 [203, 116, 81],
 [167, 41, 33],
 [166, 42, 33],
 [320, 180, 0],
 [161, 45, 31],
 [166, 122, 89],
 [164, 117, 86],
 [103, 118, 65],
 [105, 118, 69],
 [117, 36, 53],
 [158, 77, 153],
 [106, 118, 70],
 [209, 122, 75],
 [320, 180, 0],
 [105, 85, 63],
 [107, 86, 62],
 [320, 180, 0],
 [104, 118, 65],
 [114, 35, 52],
 [320, 180, 0],
 [320, 180, 0]
]

# create command
class yeet(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="yeet")
    async def yeet(self, context, member: discord.Member = None):
        #loading
        await context.message.add_reaction("🇱")
        await context.message.add_reaction("🇴")
        await context.message.add_reaction("🇦")
        await context.message.add_reaction("🇩")
        await context.message.add_reaction("🇮")
        await context.message.add_reaction("🇳")
        await context.message.add_reaction("🇬")
        #open profile pictures
        pfp = Image.open(requests.get(member.avatar_url, stream=True).raw) #open img to put on astley's face
        currentSize = 128
        pfp.thumbnail(currentSize, currentSize, Image.ANTIALIAS)

        outputDir = config["root_dir"] + "temp/" + ''.join(random.choice(string.ascii_lowercase) for i in range(6))
        os.mkdir(outputDir)

        #loop through frames
        for frame in range(0, len(mapping)):
            videoFrame = Image.open(framesDir + "frame" + str(frame) + ".jpg") #open frame
            newFrame = videoFrame.copy() #create copy of new frame
            if (mapping[frame][2] != currentSize):
                pfp.thumbnail(mapping[frame][2], mapping[frame][2], Image.ANTIALIAS)
                currentSize = mapping[frame][2]
            newFrame.paste(pfp, (mapping[frame][0], mapping[frame][1])) #add profile pictures
            newFrame.save(outputDir + "/frame" + "0" * (2 - len(str(frame))) + str(frame) + ".png", format="png")

        #stitch frames together
        finalVideo = config["root_dir"] + "temp/rickroll" + str(context.message.author.id)[:4] + ".mp4"
        os.system("ffmpeg -r 20 -f image2 -s 1280x720 -i " + outputDir + "/frame%02d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p " + outputDir + ".mp4 -loglevel 0")

        os.system("ffmpeg -i " + outputDir + ".mp4 -i " + soundFile + " -map 0:v -map 1:a -c:v copy -shortest " + finalVideo + " -loglevel 0")
        await context.message.channel.send(file=discord.File(finalVideo))
        await context.message.clear_reactions() #clear loading message
        shutil.rmtree(outputDir)
        os.remove(outputDir + ".mp4")
        os.remove(finalVideo)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(yeet(bot))