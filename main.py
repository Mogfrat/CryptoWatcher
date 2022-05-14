#Version 2.2
import discord
from discord import embeds
from discord.ext.commands.bot import Bot
from discord.user import *
from discord.ext import commands
import requests
import json
import calcul
#import graph

#Constante :
TOKEN = open("token.json")
TOKEN1 = json.load(TOKEN)
CLIENT = discord.Client()
BOT = commands.Bot(command_prefix='*')

#Connexion
@BOT.event
async def on_ready():
    await BOT.change_presence(activity=discord.Activity(type = discord.ActivityType.watching , name="Crypto"))
    print("bot is op")

#Commande pour connaitres les infos sur le mineur sur ethermine (Paiement par le réseau matic)
@BOT.command()
async def etherminePol(ctx, miner) :
    t = requests.get("https://api.ethermine.org/miner/"+miner+"/dashboard").json()
    currentHashrate = t["data"]["currentStatistics"]["currentHashrate"]
    reportedHashrate = t["data"]["currentStatistics"]["reportedHashrate"]
    validShares = t["data"]["currentStatistics"]["validShares"]
    invalidShares = t["data"]["currentStatistics"]["invalidShares"]
    stalesShares = t["data"]["currentStatistics"]["staleShares"]
    activeWorkers = t["data"]["currentStatistics"]["activeWorkers"]
    tUnpaid = t["data"]["currentStatistics"]["unpaid"]

    t2 = requests.get("https://api.ethermine.org/miner/"+miner+"/currentStats").json()
    averageHashrate = t2["data"]["averageHashrate"]
    ethPerMin = t2["data"]["coinsPerMin"]
    NxtPayout = calcul.nxtPayoutPol(tUnpaid=tUnpaid, ethPerMin=ethPerMin)
    temp = str(NxtPayout)
    if float(temp[2]) >= 5 :
       NxtPayout = calcul.ceil(NxtPayout)
       temps = " Jour(s)"
    else :
        NxtPayout = calcul.floor(NxtPayout)
        temps = " Jour(s)"
        if NxtPayout <= 0.5 :
            NxtPayout = calcul.nxtPayout_min()
            if float(temp[2]) >= 5 :
                NxtPayout = calcul.ceil(NxtPayout)
                temps = " Heure(s)"
            else :
                NxtPayout = calcul.floor(NxtPayout)
                temps = " Heure(s)"

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles du mineur sur la pool d'ethermine")
    embed.set_image(url="https://www.cryptohunters.biz/wp-content/uploads/China-Targets-Crypto-Mining-at-State-Owned-Enterprises-Threatens-Punitive-Measures.jpg")
    embed.add_field(name="Hashrate moyen :", value= "{:.6f}".format(averageHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate actuel :", value= str(currentHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate affiché :", value= str(reportedHashrate/1000000) + " MH/s", inline=True)
    embed.add_field(name="Partage valide :", value= validShares, inline=True)
    embed.add_field(name="Partage invalide :", value= invalidShares, inline=True)
    embed.add_field(name="Partage en retard :", value= stalesShares, inline=True)
    embed.add_field(name="Worker actif :", value= activeWorkers, inline=True)
    embed.add_field(name="Impayé :", value= "{:.6f}".format(calcul.unpaid)  + " eth", inline=True)
    embed.add_field(name="Prochain paiement :", value= "±" + str(NxtPayout) + temps , inline=True)
    await ctx.send(embed=embed)


#Commande pour connaitres les infos sur le mineur sur ethermine (Paiement par le réseau ethereum)
@BOT.command()
async def ethermine(ctx, miner) :
    t = requests.get("https://api.ethermine.org/miner/"+miner+"/dashboard").json()
    currentHashrate = t["data"]["currentStatistics"]["currentHashrate"]
    reportedHashrate = t["data"]["currentStatistics"]["reportedHashrate"]
    validShares = t["data"]["currentStatistics"]["validShares"]
    invalidShares = t["data"]["currentStatistics"]["invalidShares"]
    stalesShares = t["data"]["currentStatistics"]["staleShares"]
    activeWorkers = t["data"]["currentStatistics"]["activeWorkers"]
    tUnpaid = t["data"]["currentStatistics"]["unpaid"]
    payout = t["data"]["settings"]["minPayout"]

    t2 = requests.get("https://api.ethermine.org/miner/"+miner+"/currentStats").json()
    averageHashrate = t2["data"]["averageHashrate"]
    ethPerMin = t2["data"]["coinsPerMin"]
    NxtPayout = calcul.nxtPayout(payout=payout, tUnpaid=tUnpaid, ethPerMin=ethPerMin)
    temp = str(NxtPayout)
    if float(temp[2]) >= 5 :
       NxtPayout = calcul.ceil(NxtPayout)
       temps = " Jour(s)"
    else :
        NxtPayout = calcul.floor(NxtPayout)
        temps = " Jour(s)"
        if NxtPayout < 0 :
            NxtPayout = calcul.nxtPayout_min()
            if float(temp[2]) >= 5 :
                NxtPayout = calcul.ceil(NxtPayout)
                temps = " Heure(s)"
            else :
                NxtPayout = calcul.floor(NxtPayout)
                temps = " Heure(s)"

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles du mineur sur la pool d'ethermine")
    embed.set_image(url="https://www.cryptohunters.biz/wp-content/uploads/China-Targets-Crypto-Mining-at-State-Owned-Enterprises-Threatens-Punitive-Measures.jpg")
    embed.add_field(name="Hashrate moyen :", value= "{:.6f}".format(averageHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate actuel :", value= str(currentHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate affiché :", value= str(reportedHashrate/1000000) + " MH/s", inline=True)
    embed.add_field(name="Partage valide :", value= validShares, inline=True)
    embed.add_field(name="Partage invalide :", value= invalidShares, inline=True)
    embed.add_field(name="Partage en retard :", value= stalesShares, inline=True)
    embed.add_field(name="Worker actif :", value= activeWorkers, inline=True)
    embed.add_field(name="Impayé :", value= "{:.6f}".format(calcul.unpaid)  + " eth", inline=True)
    embed.add_field(name="Prochain paiement :", value= "±" + str(NxtPayout) + temps , inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def statsEthermine(ctx) :
    t = requests.get("https://api.ethermine.org/poolStats").json()
    hashrate = t["data"]["poolStats"]["hashRate"]
    miners = t["data"]["poolStats"]["miners"]
    workers = t["data"]["poolStats"]["workers"]
    blockPerHour = t["data"]["poolStats"]["blocksPerHour"]
    nbLastMinedBlock = t["data"]["minedBlocks"][0]["number"]
    minerLastMinedBlock = t["data"]["minedBlocks"][0]["miner"]

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles de la pool d'ethermine")     
    embed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.investirbitcoin.fr%2Fwp-content%2Fuploads%2F2020%2F12%2FLe-plus-ancien-pool-de-minage-Bitcoin-immortalise-un.jpg&f=1&nofb=1")
    embed.add_field(name="Hashrate :", value= "{:.6f}".format(hashrate/1000000000000) + " TH/s" , inline=True)
    embed.add_field(name="Mineur actifs :", value= str(miners) + " Mineurs" , inline=True)
    embed.add_field(name="Workers actifs :", value= str(workers) + " workers", inline=True)
    embed.add_field(name="Blocks par heure :", value= blockPerHour, inline=True)
    embed.add_field(name="Numéro du dernier block miné :", value= nbLastMinedBlock, inline=True)
    embed.add_field(name="Mineur ayant miné le dernier block :", value= minerLastMinedBlock, inline=True)
    await ctx.send(embed=embed)

#Commande pour connaitres les infos sur le mineur sur nanopool
@BOT.command()
async def nanopool(ctx, miner) :
    t = requests.get("https://api.nanopool.org/v1/eth/user/"+miner).json()
    currentHashrate = t["data"]["hashrate"]
    activeWorkers = t["data"]["workers"]
    activeWorkers = len(activeWorkers)
    tUnpaid = t["data"]["balance"]
    averageHashrate = t["data"]["avgHashrate"]["h24"]

    t2 = requests.get("https://api.nanopool.org/v1/eth/reportedhashrate/"+miner).json()
    reportedHashrate = t2["data"]

    t3 = requests.get("https://api.nanopool.org/v1/eth/usersettings/"+miner).json()


    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles du mineur sur la pool de nanopool")
    embed.set_image(url="https://www.cryptohunters.biz/wp-content/uploads/China-Targets-Crypto-Mining-at-State-Owned-Enterprises-Threatens-Punitive-Measures.jpg")
    embed.add_field(name="Hashrate moyen :", value= averageHashrate  + " MH/s" , inline=True)
    embed.add_field(name="Hashrate actuel :", value= currentHashrate + " MH/s" , inline=True)
    embed.add_field(name="Hashrate affiché :", value= str(reportedHashrate) + " MH/s" , inline=True)
    embed.add_field(name="Worker actif :", value= activeWorkers, inline=True)
    embed.add_field(name="Impayé :", value= tUnpaid  + " eth", inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def statsNanopool(ctx) :
    t = requests.get("https://api.nanopool.org/v1/eth/pool/activeminers").json()
    miners = t["data"]

    t2 = requests.get("https://api.nanopool.org/v1/eth/pool/activeworkers").json()
    workers = t2["data"]

    t3 = requests.get("https://api.nanopool.org/v1/eth/pool/hashrate").json()
    hashrate = t3["data"]/1000000

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles de la pool de nanopool")     
    embed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.investirbitcoin.fr%2Fwp-content%2Fuploads%2F2020%2F12%2FLe-plus-ancien-pool-de-minage-Bitcoin-immortalise-un.jpg&f=1&nofb=1")
    embed.add_field(name="Hashrate :", value= "{:.6f}".format(hashrate) + " TH/s" , inline=True)
    embed.add_field(name="Mineur actifs :", value= str(miners) + " Mineurs" , inline=True)
    embed.add_field(name="Workers actifs :", value= str(workers) + " workers", inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def flexpool(ctx, miner):
    t = requests.get("https://api.flexpool.io/v2/miner/stats?coin=eth&address="+miner).json()
    averageHashrate = t["result"]["averageEffectiveHashrate"]
    currentHashrate = t["result"]["currentEffectiveHashrate"]
    reportedHashrate = t["result"]["reportedHashrate"]
    validShares = t["result"]["validShares"]
    invalidShares = t["result"]["invalidShares"]
    staleShares = t["result"]["staleShares"]

    t2= requests.get("https://api.flexpool.io/v2/miner/balance?coin=eth&address="+miner).json()
    unpaid = t2["result"]["balance"]/1000000000000000000

    t3 = requests.get("https://api.flexpool.io/v2/miner/workerCount?coin=eth&address="+miner).json()
    activeWorkers = t3["result"]["workersOnline"]

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles du mineur sur la pool de flexpool")
    embed.set_image(url="https://www.cryptohunters.biz/wp-content/uploads/China-Targets-Crypto-Mining-at-State-Owned-Enterprises-Threatens-Punitive-Measures.jpg")
    embed.add_field(name="Hashrate moyen :", value= "{:.6f}".format(averageHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate actuel :", value= str(currentHashrate/1000000) + " MH/s" , inline=True)
    embed.add_field(name="Hashrate affiché :", value= str(reportedHashrate/1000000) + " MH/s", inline=True)
    embed.add_field(name="Partage valide :", value= validShares, inline=True)
    embed.add_field(name="Partage invalide :", value= invalidShares, inline=True)
    embed.add_field(name="Partage en retard :", value= staleShares, inline=True)
    embed.add_field(name="Worker actif :", value= activeWorkers, inline=True)
    embed.add_field(name="Impayé :", value= "{:.6f}".format(unpaid)  + " eth", inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def statsFlexpool(ctx) :
    t = requests.get("https://api.flexpool.io/v2/pool/hashrate?coin=eth").json()
    hashrate = t["result"]["total"]/1000000000000

    t2 = requests.get("https://api.flexpool.io/v2/pool/minerCount?coin=eth").json()
    miners = t2["result"]

    t3 = requests.get("https://api.flexpool.io/v2/pool/workerCount?coin=eth").json()
    workers = t3["result"]

    embed=discord.Embed(title="Miner info", description="Cette commande affiche les informations actuelles de la pool de Flexpool")     
    embed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.investirbitcoin.fr%2Fwp-content%2Fuploads%2F2020%2F12%2FLe-plus-ancien-pool-de-minage-Bitcoin-immortalise-un.jpg&f=1&nofb=1")
    embed.add_field(name="Hashrate :", value= "{:.6f}".format(hashrate) + " TH/s" , inline=True)
    embed.add_field(name="Mineur actifs :", value= str(miners) + " Mineurs" , inline=True)
    embed.add_field(name="Workers actifs :", value= str(workers) + " workers", inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def cryptoinfo(ctx, crypto) :
    t = requests.get("https://data.messari.io/api/v1/assets/"+crypto+"/metrics").json()
    name = t["data"]["symbol"]
    dollar = t["data"]["market_data"]["price_usd"]
    btc = t["data"]["market_data"]["price_btc"]
    eth = t["data"]["market_data"]["price_eth"]
    high1h = t["data"]["market_data"]["ohlcv_last_1_hour"]["high"]
    low1h = t["data"]["market_data"]["ohlcv_last_1_hour"]["low"]
    high24h = t["data"]["market_data"]["ohlcv_last_24_hour"]["high"]
    low24h = t["data"]["market_data"]["ohlcv_last_24_hour"]["low"]
    nbOfWhales  = t["data"]["on_chain_data"]["addresses_balance_greater_1k_native_units_count"]
    nbOfHumpback = t["data"]["on_chain_data"]["addresses_balance_greater_10k_native_units_count"]

    embed=discord.Embed(title="Crypto info", description="Cette commande affiche les informations actuelles sur " + name)
    embed.set_image(url="https://bitrazzi.com/wp-content/uploads/2018/07/Depositphotos_174996676_l-2015-750x430.jpg")
    embed.add_field(name="Valeur en dollar :", value= "{:.4f}".format(dollar), inline=True)
    embed.add_field(name="Valeur en bitcoin :", value= "{:.6f}".format(btc), inline=True)
    embed.add_field(name="Valeur en eth :", value= "{:.6f}".format(eth), inline=True)
    embed.add_field(name="Prix le plus haut 1h :", value= "{:.4f}".format(high1h), inline=True)
    embed.add_field(name="Prix le plus bas 1h :", value= "{:.4f}".format(low1h), inline=True)
    embed.add_field(name="Prix le plus haut 24h :", value= "{:.4f}".format(high24h), inline=True)
    embed.add_field(name="Prix le plus bas 24h :", value= "{:.4f}".format(low24h), inline=True)
    embed.add_field(name="Nombre de baleines :", value= nbOfWhales, inline=True)
    embed.add_field(name="Nombre de Humpback :", value= nbOfHumpback, inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def balancem(ctx, wallet):
    t = requests.get("https://api.polygonscan.com/api?module=account&action=balance&address="+wallet+"&tag=latest&apikey="+TOKEN1["polScan"]).json()
    montant = int(t["result"])/1000000000000000000
    embed=discord.Embed(title="Wallet info", description="Cette commande affiche le montant en matic sur le wallet sur le réseau matic")
    embed.add_field(name="Montant sur ce wallet : ", value= str("{:.6f}".format(montant)) + "Matic", inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def balancee(ctx, wallet):
    t = requests.get("https://api.etherscan.io/api?module=account&action=balance&address="+wallet+"&tag=latest&apikey="+TOKEN1["ethScan"]).json()
    montant = int(t["result"])/1000000000000000000
    embed=discord.Embed(title="Wallet info", description="Cette commande affiche le montant en eth sur le wallet sur le réseau ethereum")
    embed.add_field(name="Montant sur ce wallet : ", value= str("{:.6f}".format(montant)) + "Eth", inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def gas(ctx, network):
    
    t = requests.get("https://api.zapper.fi/v1/gas-price?network="+network+"&api_key="+TOKEN1["zapper"]).json()
    embed=discord.Embed(title="Gas info", description="Cette commande affiche les différents prix du gas")
    embed.add_field(name="Lent :", value= "🐢 " + str(t["standard"]), inline=True)
    embed.add_field(name="Moyen : ", value= "🚶 " + str(t["fast"]), inline=False)
    embed.add_field(name="Rapide : ", value= "⚡ " + str(t["instant"]), inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def github(ctx):
    embed=discord.Embed(title="Github repo", description="Cette commande affiche le repo du bot")
    embed.set_image(url="https://www.kynetics.com/docs/2018/images/open-source-heading.jpg")
    embed.add_field(name="Le repo :", value= "https://github.com/Mogfrat/CryptoWatcher", inline=True)
    await ctx.send(embed=embed)


@BOT.command()
async def aave(ctx, adress, network):
    t = requests.get("https://api.zapper.fi/v1/protocols/aave-v2/balances?addresses%5B%5D="+adress+"&network="+network+"&api_key="+TOKEN1["zapper"]).json()

    embed=discord.Embed(title= t[adress.lower()]["products"][0]["label"], description="Affiche le montant du wallet du total, du dépôt et d'emprunt sur aave")
    embed.set_thumbnail(url="https://storage.googleapis.com/zapper-fi-assets/apps/aave-v2.png")
    embed.add_field(name="Réseau :", value= network, inline=True)
    embed.add_field(name=t[adress.lower()]["meta"][0]["label"], value= t[adress.lower()]["meta"][0]["value"], inline=False)
    embed.add_field(name=t[adress.lower()]["meta"][1]["label"] , value= t[adress.lower()]["meta"][1]["value"], inline=False)
    embed.add_field(name=t[adress.lower()]["meta"][2]["label"] , value= abs(t[adress.lower()]["meta"][2]["value"]), inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def aavedep(ctx, adress, network):
    t = requests.get("https://api.zapper.fi/v1/protocols/aave-v2/balances?addresses%5B%5D="+adress+"&network="+network+"&api_key="+TOKEN1["zapper"]).json()

    embed = discord.Embed(title= t[adress.lower()]["products"][0]["label"], description ="Affiche les cryptos qui sont déposés sur le protocole aave")
    embed.set_thumbnail(url="https://storage.googleapis.com/zapper-fi-assets/apps/aave-v2.png")
    embed.add_field(name = t[adress.lower()]["products"][0]["assets"][0]["label"], value= t[adress.lower()]["products"][0]["assets"][0]["tokens"][0]["balance"], inline=False)
    embed.add_field(name=t[adress.lower()]["products"][0]["assets"][2]["label"], value=t[adress.lower()]["products"][0]["assets"][2]["tokens"][0]["balance"], inline=False)
    embed.add_field(name=t[adress.lower()]["products"][0]["assets"][4]["label"], value=t[adress.lower()]["products"][0]["assets"][4]["tokens"][0]["balance"], inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def aaveemp(ctx, adress, network):
    t = requests.get("https://api.zapper.fi/v1/protocols/aave-v2/balances?addresses%5B%5D="+adress+"&network="+network+"&api_key="+TOKEN1["zapper"]).json()

    embed = discord.Embed(title= t[adress.lower()]["products"][0]["label"], description ="Affiche les cryptos qui sont empruntés sur le protocole aave")
    embed.set_thumbnail(url="https://storage.googleapis.com/zapper-fi-assets/apps/aave-v2.png")
    embed.add_field(name = t[adress.lower()]["products"][0]["assets"][1]["label"], value= t[adress.lower()]["products"][0]["assets"][1]["tokens"][0]["balance"], inline=False)
    embed.add_field(name=t[adress.lower()]["products"][0]["assets"][3]["label"], value=t[adress.lower()]["products"][0]["assets"][3]["tokens"][0]["balance"], inline=False)
    embed.add_field(name=t[adress.lower()]["products"][0]["assets"][5]["label"], value=t[adress.lower()]["products"][0]["assets"][5]["tokens"][0]["balance"], inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def aaverew(ctx, adress, network):
    t = requests.get("https://api.zapper.fi/v1/protocols/aave-v2/balances?addresses%5B%5D="+adress+"&network="+network+"&api_key="+TOKEN1["zapper"]).json()

    embed = discord.Embed(title= t[adress.lower()]["products"][0]["label"], description ="Affiche les cryptos qui ont été générés sur le protocole aave")
    embed.set_thumbnail(url="https://storage.googleapis.com/zapper-fi-assets/apps/aave-v2.png")
    embed.add_field(name = t[adress.lower()]["products"][0]["assets"][6]["type"], value= t[adress.lower()]["products"][0]["assets"][6]["tokens"][0]["balance"], inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def aaveinfo(ctx):
    embed=discord.Embed(title="Aave info", description="Cette commande affiche les commandes liées au protocole aave")
    embed.set_thumbnail(url="https://storage.googleapis.com/zapper-fi-assets/apps/aave-v2.png")
    embed.add_field(name="Afficher les informations sur le dépot, l'emprunt et différence des deux :", value= "*aave [wallet] [réseau]", inline=False)
    embed.add_field(name="Afficher les informations sur les cryptos déposées sur le protocole aave :", value= "*aavedep [wallet] [réseau]", inline=False)
    embed.add_field(name="Afficher les informations sur les cryptos umpruntées sur le protocole aave :", value= "*aaveemp [wallet] [réseau]", inline=False)
    embed.add_field(name="Afficher les informations sur les cryptos générés sur le protocole aave :", value= "aaverew [wallet] [réseau]", inline=False)
    await ctx.send(embed=embed)


@BOT.command()
async def protocole(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 0
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 :
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole2(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 25
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 :
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole3(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 75
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 : 
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole4(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 100
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 :
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole5(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 125
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 : 
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole6(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 150
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 : 
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def protocole7(ctx):
    t = requests.get("https://api.zapper.fi/v1/apps?api_key=96e0cc51-a62e-42ca-acee-910ea7d2a241").json()
    x = 175
    embed=discord.Embed(title="Protocols info :", description="")
    while x <= 195 :
        try :
            embed.add_field(name= t[x]["id"], value= t[x]["supportedNetworks"][0]["network"], inline=True)
        except IndexError :
            pass
        x = x + 1
    await ctx.send(embed=embed)


@BOT.command()
async def aide(ctx):
    embed=discord.Embed(title="Aide info", description="Cette commande affiche les commandes disponibles")
    embed.add_field(name="Afficher les informations de son miner sur ethermine :", value= "*ethermine [wallet]", inline=False)
    embed.add_field(name="Afficher les informations sur la pool d'ethermine :", value= "*statsEthermine", inline=False)
    embed.add_field(name="Afficher les informations de son miner sur nanopool :", value= "*nanopool [wallet]", inline=False)
    embed.add_field(name="Afficher les informations sur la pool de nanopool :", value= "*statsNanopool", inline=False)
    embed.add_field(name="Afficher les informations de son miner sur Flexpool :", value= "*Flexpool [wallet]", inline=False)
    embed.add_field(name="Afficher les informations sur la pool de FLexpool :", value= "*statsFlexpool", inline=False)
    embed.add_field(name="Afficher les différentes informations d'une crypto monnaie : ", value= "*cryptoinfo [Nom/symbole de la crypto]", inline=False)
    embed.add_field(name="Afficher le montant en matic dans le wallet sur le réseau matic : ", value= "*balancem [wallet]", inline=False)
    embed.add_field(name="Afficher le montant en eth dans le wallet sur le réseau ethereum : ", value= "*balancee [wallet]", inline=False)
    embed.add_field(name="Afficher le nombre de GWei pour les différentes vitesse de transaction sur le réseau ethereum : ", value= "*gas", inline=False)
    embed.add_field(name="Afficher les différentes commandes lié au protocole aave : ", value= "*aaveinfo", inline=False)
    embed.add_field(name="Afficher le repo du bot: ", value= "*github", inline=False)
    await ctx.send(embed=embed)


BOT.run(TOKEN1["discord_api"])