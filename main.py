import os
import logging
import discord
from discord.ext import commands, tasks
from discord import Embed
from datetime import datetime, timedelta
import random

# Setup logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# List of Duas
duas = [
    {"name": "Dua for Guidance", "text": "اللّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى", "translation": "O Allah! I ask You for guidance, piety, chastity and self-sufficiency."},
    {"name": "Dua for Forgiveness", "text": "رَبَّنَا ظَلَمْنَا أَنفُسَنَا وَإِن لَّمْ تَغْفِرْ لَنَا وَتَرْحَمْنَا لَنَكُونَنَّ مِنَ الْخَاسِرِينَ", "translation": "Our Lord, we have wronged ourselves, and if You do not forgive us and have mercy upon us, we will surely be among the losers."},
    {"name": "Dua Before Sleeping", "text": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "translation": "In Your name, O Allah, I die and I live."},
    {"name": "Dua Upon Waking Up", "text": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", "translation": "Praise is to Allah Who gives us life after He has caused us to die and to Him is the return."},
    {"name": "Dua Before Eating", "text": "بِسْمِ اللَّهِ", "translation": "In the name of Allah."},
    {"name": "Dua After Eating", "text": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مُسْلِمِينَ", "translation": "Praise is to Allah Who has given us food and drink and made us Muslims."},
    {"name": "Dua Before Entering Bathroom", "text": "بِسْمِ اللَّهِ، اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبُثِ وَالْخَبَائِثِ", "translation": "In the name of Allah, O Allah, I seek refuge with You from all evil and evil-doers."},
    {"name": "Dua After Leaving Bathroom", "text": "غُفْرَانَكَ", "translation": "I seek Your forgiveness."},
    {"name": "Dua for Travelling", "text": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ", "translation": "Glory to Him Who has subjected this to us, and we could never have it by our efforts. And to our Lord, surely, we must return."},
    {"name": "Dua for Entering Home", "text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ الْمَوْلِجِ وَخَيْرَ الْمَخْرَجِ، بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى اللَّهِ رَبِّنَا تَوَكَّلْنَا", "translation": "O Allah, I ask You for the good of entering and the good of exiting. In the name of Allah, we enter and in the name of Allah, we exit, and upon Allah, our Lord, we rely."},
    {"name": "Dua for Seeking Knowledge", "text": "رَبِّ زِدْنِي عِلْمًا", "translation": "My Lord, increase me in knowledge."},
    {"name": "Dua for Protection", "text": "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ", "translation": "In the name of Allah, with Whose name nothing in the earth or the heaven can cause harm, and He is the All-Hearing, the All-Knowing."},
    {"name": "Dua for Patience", "text": "رَبَّنَا أَفْرِغْ عَلَيْنَا صَبْرًا وَثَبِّتْ أَقْدَامَنَا وَانصُرْنَا عَلَى الْقَوْمِ الْكَافِرِينَ", "translation": "Our Lord, pour upon us patience and make our steps firm and assist us against the disbelieving people."},
    {"name": "Dua for Parents", "text": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا", "translation": "My Lord, have mercy upon them as they brought me up [when I was] small."},
    {"name": "Dua for Success", "text": "اللّهُمَّ لَا سَهْلَ إِلَّا مَا جَعَلْتَهُ سَهْلًا وَأَنْتَ تَجْعَلُ الْحَزْنَ إِذَا شِئْتَ سَهْلًا", "translation": "O Allah, there is no ease except in that which You have made easy, and You can make sorrow, if You wish, easy."},
    {"name": "Dua for Anxiety", "text": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ وَأَعُوذُ بِكَ مِنَ الْعَجْزِ وَالْكَسَلِ وَأَعُوذُ بِكَ مِنَ الْجُبْنِ وَالْبُخْلِ وَأَعُوذُ بِكَ مِنْ غَلَبَةِ الدَّيْنِ وَقَهْرِ الرِّجَالِ", "translation": "O Allah, I seek refuge in You from worry and sorrow, from weakness and laziness, from miserliness and cowardice, from being overcome by debt and overpowered by men."},
    {"name": "Dua for Gratitude", "text": "اللّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ", "translation": "O Allah, assist me in remembering You, in thanking You, and in worshiping You in the best of manners."},
    {"name": "Dua for Entering the Mosque", "text": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ", "translation": "O Allah, open the doors of Your mercy for me."},
    {"name": "Dua for Leaving the Mosque", "text": "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ", "translation": "O Allah, I ask You for Your bounty."},
    {"name": "Dua for the Sick", "text": "أَسْأَلُ اللَّهَ الْعَظِيمَ رَبَّ الْعَرْشِ الْعَظِيمِ أَنْ يَشْفِيَكَ", "translation": "I ask Allah the Magnificent, Lord of the Magnificent Throne, to cure you."},
    {"name": "Dua for Rain", "text": "اللَّهُمَّ صَيِّبًا نَافِعًا", "translation": "O Allah, (bring) beneficial rain clouds."},
    {"name": "Dua After Rain", "text": "مُطِرْنَا بِفَضْلِ اللَّهِ وَرَحْمَتِهِ", "translation": "We have been given rain by the grace and mercy of Allah."},
    {"name": "Dua for Istikhara", "text": "اللَّهُمَّ إِنِّي أَسْتَخِيرُكَ بِعِلْمِكَ وَأَسْتَقْدِرُكَ بِقُدْرَتِكَ وَأَسْأَلُكَ مِنْ فَضْلِكَ الْعَظِيمِ، فَإ ِنَّكَ تَقْدِرُ وَلَا أَقْدِرُ، وَتَعْلَمُ وَلَا أَعْلَمُ، وَأَنْتَ عَلَّامُ الْغُيُوبِ", "translation": "O Allah, I seek Your guidance [in making a choice] by virtue of Your knowledge, and I seek ability by virtue of Your power, and I ask You of Your great bounty. You have power, I have none. And You know, I know not. You are the Knower of hidden things."},
    {"name": "Dua for the Deceased", "text": "اللَّهُمَّ اغْفِرْ لَهُ وَارْحَمْهُ وَعَافِهِ وَاعْفُ عَنْهُ وَأَكْرِمْ نُزُلَهُ وَوَسِّعْ مُدْخَلَهُ وَاغْسِلْهُ بِالْمَاءِ وَالثَّلْجِ وَالْبَرَدِ وَنَقِّهِ مِنَ الْخَطَايَا كَمَا يُنَقَّى الثَّوْبُ الْأَبْيَضُ مِنَ الدَّنَسِ", "translation": "O Allah, forgive him and have mercy on him, excuse him and pardon him, and make honorable his reception. Expand his entry, cleanse him with water, snow, and ice, and purify him of sin as a white robe is purified of filth."},
]

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    send_daily_dua.start()  # Start the daily Dua task

@tasks.loop(hours=24)
async def send_daily_dua():
    # Channel ID where the bot will send the daily Dua
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = bot.get_channel(channel_id)

    if not channel:
        logging.error("Channel not found.")
        return

    # Choose a random Dua from the list
    dua = random.choice(duas)

    # Create an embedded message with Markdown
    embed = Embed(title=f"**{dua['name']}**", description=f"**Arabic:**\n{dua['text']}\n\n**Translation:**\n{dua['translation']}", color=0x00ff00)
    embed.set_footer(text="Islamic Daily Dua Bot")

    # Send the embedded message
    await channel.send(embed=embed)

@send_daily_dua.before_loop
async def before():
    await bot.wait_until_ready()
    now = datetime.utcnow()
    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    seconds_until_target = (target_time - now).total_seconds()
    await discord.utils.sleep_until(target_time)
    send_daily_dua.change_interval(hours=24, seconds=seconds_until_target)

try:
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("No token found. Please add your token to the environment variables.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        logging.error("The Discord servers denied the connection for making too many requests")
        logging.error("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
except ValueError as e:
    logging.error(e)
```
