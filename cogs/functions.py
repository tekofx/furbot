# Contains all functions that are not commands
import discord
from discord.ext import commands
from PIL import Image
import os
import moviepy.editor as mp
import logging, coloredlogs
import wget
import time
from dotenv import load_dotenv
import praw
import random




memeTemplatesPath = "memes_templates/"
memePath = "memes/"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
villa_furrense = os.getenv('VILLA_FURRENSE')
creator=os.getenv('BOT_CREATOR')

reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                     user_agent=os.getenv("REDDIT_USER_AGENT"))

def setup_logs():
    """ logger = init_logger(__name__, testing_mode=False)
    logger.debug('Testing mode = True') """
    # os.system("rm "+path+"logs")
    logging.basicConfig(filename="logs",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info("\n\n\nStarted furbot")


def log(type : str, message : str):
    if type=='info':
        logging.info(message)
    if type=='error':
        logging.error(message)

def get_user_avatar(user: discord.Member):
    """Downloads the avatar of a user

    Args:
        user (discord.Member): user to download avatar from
    """
    avatarUrl = user.avatar_url

    # var="wget -O %s%s %s"%(memeTemplatesPath,'01.webp', avatarUrl)
    # os.system(var)
    wget.download(avatarUrl, memeTemplatesPath + '01.webp')
    #os.remove('wget-log*') # Remove logs
    os.system('rm wget-log*')
    logging.info("Saved avatar with url " + avatarUrl + " in " + memeTemplatesPath)

def convert_pic(picture: str, imgName: str, imgSize: str):
    """Converts an image to PNG with a differents size

    Args:
        picture (str): picture to convert
        imgName (str): exported picture name
        imgSize (str): exported image size
    """
    img = Image.open(picture)

    wpercent = (imgSize / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((imgSize, hsize), Image.ANTIALIAS)

    img.save(memeTemplatesPath + imgName + '.png')


def get_user(context, user: discord.Member = None):
    """Gets user from a message

    Args:
        context ([Message]): [Message to get an avatar]
        user (discord.Member, optional): [User of a message]. Defaults to None.

    Returns:
        [str]: [user]
    """
    if user == None:
        output = context.author
    else:
        output = user

    return output


def delete_files(elements: list):
    """ Delete files needed to create a meme

    Args:
        elements (list): [files used in a meme]
    """
    for x in elements:
        if os.path.isfile(memeTemplatesPath+x):
            os.system('rm '+memeTemplatesPath + x)
    logging.info("Removed dependencies")





def create_meme(pictures: list, avatar_url: str, avatar_size: int, position: list, invert: bool):
    """ Crea un meme

    Args:
        pictures (list): [lista de imagenes, siendo pictures[0] el meme y el resto avatares]
        avatar_url (str): [url del avatar a añadir al meme]
        avatar_size (int): [tamañao al que convertir el avatar de webp a png]
        position (list): [posiciones en las que colocar las imagenes, siendo position[0] y position[1] la x,y del meme]
        invert (bool): [Si es True usa el meme como canvas, en caso contrario, usa el avatar]
    """

    var = "wget -O %s%s %s" % (memeTemplatesPath, "01.webp", avatar_url)
    os.system(var)

    # urllib.request.urlretrieve(avatar_url, memeTemplatesPath+'01.webp')
    # wget.download(str(avatar_url),memeTemplatesPath+"01.webp")

    # Convert avatar
    convert_pic(memeTemplatesPath + "01.webp", "01", avatar_size)

    if not invert:  # burn
        canvas = pictures[1]
        width, height = Image.open(memeTemplatesPath + canvas + '.png').convert("RGBA").size
    else:  # cringe
        canvas = pictures[0]
        width, height = Image.open(memeTemplatesPath + canvas + '.png').convert("RGBA").size

    output = Image.new("RGBA", (width, height))  # Create picture
    meme = Image.open(memeTemplatesPath + pictures[0] + '.png').convert("RGBA")  # Open meme picture

    # Add avatar pictures
    i = 2
    for x in pictures[1:]:
        img = Image.open(memeTemplatesPath + x + '.png').convert("RGBA")
        output.paste(img, (position[i], position[i + 1]), img)
        i += 2

    # Add meme picture
    output.paste(meme, (position[0], position[1]), meme)

    # Save final meme
    output.save(memeTemplatesPath + "output.png", "PNG")


def create_video_meme(meme: str, user: discord.Member):
    """Creates a video with a 50% transparency video meme above

    Args:
        meme (str): name of the video meme to put above
        user (discord.Member): user to put in the video
    """
    get_user_avatar(user)
    convert_pic(picture=memeTemplatesPath + '01.webp', imgName='01', imgSize=1000)

    # Create video
    memeVideo = (mp.VideoFileClip(memeTemplatesPath + meme + ".mp4")
                 .set_opacity(.5)
                 .set_pos(('center', 'center'))

                 )

    avatar = (mp.ImageClip(memeTemplatesPath + '01' + '.png')
              .set_duration(memeVideo.duration)
              .resize(height=360)
              .set_pos(('center', 'center'))
              )

    final_video = mp.CompositeVideoClip([avatar, memeVideo])
    final_video.write_videofile(memeTemplatesPath + "output.mp4")
    final_video.close()
    delete_files(('01' + '.webp', '01' + '.png'))


def get_user_role(user: discord.Member, rangos):
    output = None
    for role in user.roles:
        if str(role) in rangos:
            output = role.mention

    return str(output)


def get_user_roles(user: discord.Member, rangos):
    mention = []
    for role in user.roles:
        if role.name != "@everyone" and str(role) not in rangos:
            mention.append(role.mention)

    b = ", ".join(mention)
    return str(b)


# checks if message author is owner of the bot
def is_owner(context):
    if context.author.id==int(creator):
        return True
    else: 
        #await context.channel.send("No tienes permisos para usar este comando")
        return False





def get_reddit_image(Subreddit: str, Flair: str, Filter: str):
    """Gets a random Reddit image

    Args:
        Subreddit (str): [subreddit to get the photo from]
        Flair (str): [flair to filter by]
        Filter (str): [filter to search by]

    Returns:
        [str]: [url from a reddit image]
    """
    try:
        var = True
        while var:
            if Flair == None:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    Filter)  # Gets a random images from r/foxes with flair Pics!
            else:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    'Flair:' + Flair)  # Gets a random images from r/foxes with flair Pics!
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            if submission.url.endswith('jpg'):
                var = False
    except:
        logging.error("Error at getting images from reddit")

    return submission.url

def get_top_reddit_image(Subreddit:str, Limit:int):
    output=random.choice([x for x in reddit.subreddit(Subreddit).top("all", limit=Limit)])
    return output.url