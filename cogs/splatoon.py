import asyncio
import aiohttp
import time
import os
import random

from time import gmtime, strftime
import logging
import json
import subprocess
from disputils import BotEmbedPaginator
from discord.ext import commands
import discord
import tweepy

log = logging.getLogger()

# word of information, I use splatnet2statink to generate cookies

def mode_key(argument):
    lower = argument.lower().strip('"')
    if lower.startswith('rank'):
        return 'Ranked Battle'
    elif lower.startswith('turf') or lower.startswith('regular'):
        return 'Regular Battle'
    elif lower == 'league':
        return 'League Battle'
    elif lower == 'season':
        return 'X rank'
    else:
        raise commands.BadArgument('Unknown schedule type, try: "ranked", "season", "regular", or "league"')

def region_key(argument):
    lower = argument.lower().strip('"') 
    if lower.startswith('us') or lower.startswith('usa'):
        return 'The United States'
    elif lower.startswith('eu') or lower.startswith('europe'):
        return 'Europe'
    elif lower.startswith('jpn') or lower.startswith('japan'):
        return 'Japan'
    else:
        raise commands.BadArgument('Unknown region type, try: "usa", "europe", or "japan"')


def clouts():
    with open('mapcallouts.json') as m:
        return json.load(m)

def sr_mapredirect():
    with open('srmaps.json') as sr:
        return json.load(sr)

def abillity():
    with open('abillities.json') as a:
        return json.load(a)

def map_key(argument):
    return

class NoMatchException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, bug):
        Exception.__init__(self)
        self.bug = bug

SPLATNET_LINK = 'https://app.splatoon2.nintendo.net'

class Splatoon(commands.Cog):
    """Splatoon 2 related commands."""


    def __init__(self, bot):
        self.bot = bot


    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(error)


    def load_splat_cookie(self):
        with open('config.txt') as f:
            return json.load(f)

    async def get_schedules(self,ctx):
        #we could probably generate a new cookie here
        #as long as BackgroundtaskCog.py has the subprocess running
        await ctx.trigger_typing()
        cookie = self.load_splat_cookie()
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/schedules -O schedules.json", shell=True)
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/coop_schedules -O coop-schedules.json", shell=True)
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/coop_results -O coop-results.json", shell=True)
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/results -O result_list.json", shell=True)
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/onlineshop/merchandises -O merchandises.json", shell=True)

    def load_schedule(self):
        with open('schedules.json') as f:
            return json.load(f)

    def load_sr(self):  
        with open('coop-schedules.json') as f:
            return json.load(f)

    def load_sr_gear(self):  
        with open('coop-results.json') as f:
            return json.load(f)

    def load_results(self):  
        with open('result_list.json') as f:
            return json.load(f)

    def load_latest_result_statistics(self):
        result = self.load_results()
        cookie = self.load_splat_cookie()
        subprocess.Popen(f"wget --header='cookie: iksm_session={cookie['cookie']}' {SPLATNET_LINK}/api/results/{result['results'][0]['battle_number']} -O result.json", shell=True)
        with open('result.json') as f:
            return json.load(f)

    def load_gear(self):
        with open('merchandises.json') as f:
            return json.load(f)

    def get_tweet(self, tweetid):
        auth = tweepy.OAuthHandler(self.bot.consumer_key, self.bot.consumer_secret)
        auth.set_access_token(self.bot.access_token, self.bot.access_token_secret)

        api = tweepy.API(auth)

        tweet = api.get_status(tweetid, include_ext_alt_text=True, tweet_mode="extended")
        return tweet.extended_entities


    async def alltypes_map_schedule(self, ctx, number):
        try:
            splatoonjson = self.load_schedule()
        except json.decoder.JSONDecodeError:
            await ctx.send("I can't seem to connect to Splatnet at the moment, try the command again.")
            return None
        dict = splatoonjson
        # maybe a quick check to see if the cookie works
        if 'code' not in dict:
            pass
        else:
            return await ctx.send("can't get the schedule at the moment \U0000231b")
        regular = dict['regular']
        ranked  = dict['gachi']
        league  = dict['league']
        reg = regular[number]
        sch = dict['gachi'][1]
        rnk = ranked[number]
        lge = league[number]
        rnkmd = rnk['rule']['name']
        lgemd = lge['rule']['name']
        t1 = reg['stage_a']['name']
        t2 = reg['stage_b']['name']
        r1 = rnk['stage_a']['name']
        r2 = rnk['stage_b']['name']
        l1 = lge['stage_a']['name']
        l2 = lge['stage_b']['name']
        epoch = sch['start_time']
        #If we want to get the time remaining, we have to subtract the current epoch from the epoch recived
        timelef = gmtime(epoch-time.time())
        #now we have the time remaining
        hourlef = strftime('%H', timelef)
        minlef = strftime('%M', timelef)
        if int(hourlef) == 1:
            hour = strftime(" %H hour ", timelef)
        elif int(hourlef) == 0:
            hour = " "
        else:
            hour = strftime(" %H hours ", timelef)

        if int(minlef) == 1:
            mins = strftime("%M minute ", timelef)
        else:
            mins = strftime("%M minutes ", timelef)
        
        secs = strftime("%S seconds", timelef)
        
        if number == 0:
            titlename = f'For{hour}{mins}{secs}...'
        else:
            titlename = f'In{hour}{mins}{secs}...'

        desc = "**Ranked Battle** \n*__{0}:__* {1} and {2} \n".format(rnkmd, r1, r2) + "**League Battle** \n*__{0}:__* {1} and {2} \n".format(lgemd, l1, l2) + "**Regular Battle** \n*__Turf War:__* {0} and {1} \n".format(t1, t2)
        sched_embed = discord.Embed(title=titlename, description=desc, color=0x006AFF)
        sched_embed.set_footer(text="For the maps for the X rank season, do `,maps season`")
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    async def modetype_splatoon2_schedule(self, ctx, mode, num, modeid):
        try:
            splatoonjson = self.load_schedule()
        except json.decoder.JSONDecodeError:
            return None
        dict = splatoonjson
        if mode == 'Ranked Battle':
            md = 'Ranked'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'League Battle':
            md = 'League'
            basebatt = 'league'
            co = 0xFF004C
        elif mode == 'Regular Battle':
            md = 'Regular Battle'
            basebatt = 'regular'
            co = 0x4DFF00
        elif mode == 'X rank':
            md = 'Xrank'
            basebatt = 'gachi'
            co = 0xFF6F00
        else:
            log.info('something fucked up... fix it?')
        # just in case if the numbers can fit with the pages
        pageindex = num*3

        sch = dict[basebatt]
        sch1 = sch[0+pageindex]
        sch2 = sch[1+pageindex]
        sch3 = sch[2+pageindex]
        #When will the rotation end? We'll find out by getting the epoch first
        epoch1 = sch1['start_time']
        epoch2 = sch2['start_time']
        epoch3 = sch3['start_time']
        #If we want to get the time remaining, we have to subtract the current epoch from the epoch recived
        hour1 = strftime('%H', gmtime(epoch1-time.time()))
        hour2 = strftime('%H', gmtime(epoch2-time.time()))
        hour3 = strftime('%H', gmtime(epoch3-time.time()))
        minlef = strftime('%M', gmtime(epoch2-time.time()))
        seclef = strftime("%S", gmtime(epoch2-time.time()))
        #now we have the time remaining

        if int(minlef) == 1:
            mins = f"{minlef} minute "
        else:
            mins = f"{minlef} minutes "

        if int(seclef) == 1:
            secs = f"{seclef} second "
        else:
            secs = f"{seclef} seconds "
        
        if int(hour2) == 1:
            hour = f"In 1 hour "
        elif int(hour2) == 0:
            hour = "In "
        else:
            hour = f"In {hour2} hours "
        
        if epoch1 > time.time():
            if int(hour1) == 0:
                tl1 = f'In {mins}{secs}'
                tlx1= f'00h & {minlef}m'
            elif int(hour1) == 1:
                tl1 = f'In 1 hour {mins}{secs}'
                tlx1= f'{int(hour1)}h & {minlef}m'
            else:
                tl1 = f'In {int(hour1)} hours {mins}{secs}'
                tlx1= f'0{int(hour1)}h & {minlef}m'
        else:
            tl1 = "Current Rotation"
            tlx1= 'Current'

        tl2 = f"{hour}{mins}{secs}"
        tl3 = f"In {hour3} hours {mins}{secs}"
        tlx2 = strftime("%Hh & %Mm", gmtime(epoch2-time.time()))
        tlx3 = strftime("%Hh & %Mm", gmtime(epoch3-time.time()))

        if md == 'Xrank':
            # the old way to get the images was so slow,
            # I had to use tweepy to do this just so I can let it get the images from the status id of the tweet
            tweet=self.get_tweet(1244549931853021185)
            if modeid == 0:
                imageurl = tweet["media"][0]['media_url_https']
                modetag  = 'Splat Zones'
            elif modeid == 1:
                imageurl = tweet["media"][1]['media_url_https']
                modetag  = 'Tower Control'
            elif modeid == 2:
                imageurl = tweet["media"][2]['media_url_https']
                modetag  = 'Rainmaker'
            elif modeid == 3:
                imageurl = tweet["media"][3]['media_url_https']
                modetag  = 'Clam Blitz'
            else:
                imageurl = None
                modetag  = None
            sched_embed = discord.Embed(title='This Season for X rank', color=co)
            sched_embed.add_field(name='Schedule', value=f"{tlx1}: {sch1['rule']['name']} \n{tlx2}: {sch2['rule']['name']} \n{tlx3}: {sch3['rule']['name']}")
            sched_embed.add_field(name='Season maps', value=f"Maps for {modetag} are shown in the image below")
            sched_embed.set_image(url=imageurl)
        else:
            desc = f"**{tl1}** \n*__{sch1['rule']['name']}:__* {sch1['stage_a']['name']} and {sch1['stage_b']['name']} \n**{tl2}** \n*__{sch2['rule']['name']}:__* {sch2['stage_a']['name']} and {sch2['stage_b']['name']} \n**{tl3}** \n*__{sch3['rule']['name']}:__* {sch3['stage_a']['name']} and {sch3['stage_b']['name']} \n"
            sched_embed = discord.Embed(title='Map Schedule for {} in Splatoon 2'.format(md), description=desc, color=co)
        return sched_embed



    async def sr_schedule(self,ctx,num):
        try:
            srsch = self.load_sr()
            srGear= self.load_sr_gear()
        except json.decoder.JSONDecodeError:
            await ctx.send("I can't seem to connect to Splatnet at the moment, try the command again.")
            return None
        dict = srsch
        basedets = dict['details'][num]
        schsrtime = basedets['start_time']
        curtime = time.time()
        stagename = basedets['stage']['name']
        imageurl = basedets['stage']['image']
        weapons = basedets['weapons']
        w1id = weapons[0]['id']
        w2id = weapons[1]['id']
        w3id = weapons[2]['id']
        w4id = weapons[3]['id']

        if w1id == "-1":
            wep1 = weapons[0]['coop_special_weapon']['name']
        else:
            wep1 = weapons[0]['weapon']['name']

        if w2id == "-1":
            wep2 = weapons[1]['coop_special_weapon']['name']
        else:
            wep2 = weapons[1]['weapon']['name']

        if w3id == "-1":
            wep3 = weapons[2]['coop_special_weapon']['name']
        else:
            wep3 = weapons[2]['weapon']['name']

        if w4id == "-1":
            wep4 = weapons[3]['coop_special_weapon']['name']
        else:
            wep4 = weapons[3]['weapon']['name']

        if schsrtime > curtime:
            keyword = "Upcomming"
        else:
            keyword = "Ongoing"
        emb = discord.Embed(title=keyword+" shift for Salmon Run", description=stagename, color=0xFF8C00)
        emb.set_image(url=SPLATNET_LINK+imageurl)
        emb.add_field(name='Weapons', value=wep1+'\n'+wep2+'\n'+wep3+'\n'+wep4)
        try:
        	emb.add_field(name='Current Gear', value=f"{srGear['reward_gear']['name']}")
        	emb.set_thumbnail(url=SPLATNET_LINK+srGear['reward_gear']['image'])
        except:
        	pass
        return emb

    async def splatgear_clock(self):
        try:
            await self.get_schedules()
            embed = [await self.get_gear(ctx, 0)]
            paginator = BotEmbedPaginator(ctx, embed)
            channel = discord.utils.get(guild.channels, name='results') 

            if time.strftime('%H:%M',time.gmtime())  ==  '00:01'or'02:01'or'04:01'or'06:01'or'08:01'or'10:01'or'12:01':
                await paginator.run()
                await asyncio.sleep(60)
            elif time.strftime('%H:%M',time.gmtime()) == '14:01'or'16:01'or'18:01'or'20:01'or'22:01'or'24:01':
                await paginator.run()
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(10)
        except:
            pass

    async def splatgear_clock_test(self):
        try:
            channel = discord.utils.get(discord.abc.GuildChannel, name='splatnet') 
            await self.get_schedules(channel)
            embed = [await self.get_gear(channel, 0)]
            paginator = BotEmbedPaginator(channel, embed)
            await paginator.run()
        except:
            pass

    async def get_gear(self,ctx,itemid):
        try:
            gearjson = self.load_gear()
        except json.decoder.JSONDecodeError:
            await ctx.send("I can't seem to connect to Splatnet at the moment, try the command again.")
            return None
        dict = gearjson
        abillities = abillity()
        newgear = dict['merchandises'][itemid]
        gearname = newgear['gear']['name']
        gearthumb = newgear['gear']['image']
        gearprice = str(newgear['price'])
        gearabillity = newgear['skill']['name']
        link = SPLATNET_LINK+gearthumb
        #ids are kinda the key to show the abillity, thermal ink is 106
        if gearabillity == 'Ink Saver (Main)':
            emoji = abillities['ism']
        elif gearabillity == 'Ink Saver (Sub)':
            emoji = abillities['iss']
        elif gearabillity == 'Ink Recovery Up':
            emoji = abillities['iru']
        elif gearabillity == 'Run Speed Up':
            emoji = abillities['run']
        elif gearabillity == 'Swim Speed Up':
            emoji = abillities['swim']
        elif gearabillity == 'Special Charge Up':
            emoji = abillities['scu']
        elif gearabillity == 'Special Saver':
            emoji = abillities['ss']
        elif gearabillity == 'Special Power Up':
            emoji = abillities['spu']
        elif gearabillity == 'Quick Respawn':
            emoji = abillities['qr']
        elif gearabillity == 'Quick Super Jump':
            emoji = abillities['qsj']
        elif gearabillity == 'Sub Power Up':
            emoji = abillities['subpow']
        elif gearabillity == 'Ink Resistance Up':
            emoji = abillities['inkres']
        elif gearabillity == 'Bomb Defense Up DX':
            emoji = abillities['bdef']
        elif gearabillity == 'Main Power Up':
            emoji = abillities['mpu']
        elif gearabillity == 'Comeback':
            emoji = abillities['cbk']
        elif gearabillity == 'Opening Gambit':
            emoji = abillities['og']
        elif gearabillity == 'Last-Ditch Effort':
            emoji = abillities['lde']
        elif gearabillity == 'Tenacity':
            emoji = abillities['tena']
        elif gearabillity == 'Ninja Squid':
            emoji = abillities['ns']
        elif gearabillity == 'Haunt':
            emoji = abillities['haunt']
        elif gearabillity == 'Thermal Ink':
            emoji = abillities['ti']
        elif gearabillity == 'Respawn Punisher':
            emoji = abillities['rp']
        elif gearabillity == 'Stealth Jump':
            emoji = abillities['sj']
        elif gearabillity == 'Object Shredder':
            emoji = abillities['os']
        elif gearabillity == 'Drop Roller':
            emoji = abillities['dr']
        em = discord.Embed(title=gearname)
        em.add_field(name='Price:', value=abillities['coin']+gearprice)
        em.add_field(name='Abillity:', value=emoji+gearabillity)
        em.set_thumbnail(url=link)
        return em


    @commands.command(aliases=['maps'])
    async def schedule(self, ctx, *, type: mode_key = None):
        """Shows the current Splatoon 2 schedule."""
        if type is None:
            num = 0
            await self.get_schedules(ctx)
            await asyncio.sleep(1)
            await self.alltypes_map_schedule(ctx, num)
        else:
            try:
                await self.get_schedules(ctx)
                await asyncio.sleep(1)
                embeds = [
                    await self.modetype_splatoon2_schedule(ctx, type, 0, 0),
                    await self.modetype_splatoon2_schedule(ctx, type, 1, 1),
                    await self.modetype_splatoon2_schedule(ctx, type, 2, 2),
                    await self.modetype_splatoon2_schedule(ctx, type, 3, 3)
                ]
                paginator = BotEmbedPaginator(ctx, embeds)
                await paginator.run()
            except:
                # just in case of an error
                await ctx.send("I can't seem to connect to Splatnet at the moment, try the command again.")
                pass


    @commands.command(hidden=True)
    @commands.is_owner()
    async def advice(self, ctx):
        """just some lifechoaching for Inkx"""
        results = self.load_results()
        adviceList = ['RECHARGE YOUR INK!','Stop being on autopilot.','STOP ASKING QUESTIONS AND JUST PLAY!','STOP BLAMING OTHERS AND ACCEPT YOUR MISTAKES!']
        if results['results'][0]['my_team_result']['key'] == 'defeat':
            await ctx.send(random.choice(adviceList))
        else:
            await ctx.send("I have no advice for you "+"<:AigisSmile:596792544386613258>")

    @commands.command()
    async def nextmaps(self, ctx):
        """Shows the next Splatoon 2 maps."""
        num = 1
        try:
            await self.get_schedules(ctx)
            await self.alltypes_map_schedule(ctx, num)
        except:
            pass

    @commands.command(aliases=['sr'])
    async def salmon(self, ctx):
        """Shows the current Salmon Run shift."""
        try:
            await self.get_schedules(ctx)
            embeds = [
                await self.sr_schedule(ctx, 0),
                await self.sr_schedule(ctx, 1)
            ]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        except:
            pass

    @commands.command(aliases=['c'])
    async def callouts(self, ctx, mapname):
        """Posts an image of callouts in a map of Splatoon 2, ",callouts list" for the entire list of callouts"""
        files = clouts()
        try:
            clout = files[mapname]['map']
            name = files[mapname]['name']
            if clout == "Callout List":
                d = "reef \nfitness \nmoray \nmako \nblackbelly \ncanal \nstarfish \nhumpback \ninkblot \nmanta \nport \nsturgeon \ndome \nwalleye \narowana \nshellendorf \ngoby \npit \npitrm \ncamp \nwahoo \nhotel \nanchov \nskipper"
                em = discord.Embed(title='List of Map Callouts', description=d, color=0xFF8C00)
            elif clout=="All Maps":
                url = "https://drive.google.com/drive/folders/0B3prVTgFFXASZm1EQkdFbk1JYVk"
                em = discord.Embed(title=f'Click here for all callouts', color=0xFF8C00, url=url)
            else:
                em = discord.Embed(title=f"Callouts for {name}", color=0xFF8C00, url=clout)
                em.set_image(url=clout)
        except KeyError:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That's nothing in my database.")
            em = None
        finally:
            try:
                if em == None:
                    pass
                else:
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send(embed=em)
            except commands.MissingPermissions:
                await ctx.send("I don't have permission to embed links!")

    @commands.command()
    async def splatfest(self, ctx, *, type: region_key = None):
        """Shows information about the currently running Splatfests, if any. Defaults to us."""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("Fool! Theres no more Splatfests!")

    @commands.command()
    async def splatnet(self, ctx):
        """Shows the current items from Annie's Online Store"""
        try:
            await self.get_schedules(ctx)
            embeds = [
                await self.get_gear(ctx, 0),
                await self.get_gear(ctx, 1),
                await self.get_gear(ctx, 2),
                await self.get_gear(ctx, 3),
                await self.get_gear(ctx, 4),
                await self.get_gear(ctx, 5)
            ]
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        except:
            pass
    
def setup(bot):
    bot.add_cog(Splatoon(bot))
