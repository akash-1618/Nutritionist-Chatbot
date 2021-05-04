import aiml
import discord
from discord.ext import commands
import asyncio
import random
import os
import csv
import re
from random import randint
from difflib import SequenceMatcher
from goto import with_goto


#--------------TYPE YOUR TOKEN AND OTHER STUFF BELOW--------------#
f = open('token.txt','r') #store your token in a separate text file in the same folder
token = f.read()
f.close()

TOKEN = token # your token

channel_name = "your-channel-name-goes-here" # default channel name

server_name = "your-server-name-goes-here"   # server name

invite_link = "invite_link_of_your_chatbot"

colour = 0xffb7c5 # default colour for embeds

#-----------------------------------------------------------------#

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco

def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#-----------------------------------------------------------------#
prefix = "!!"
client1 = commands.Bot(command_prefix=prefix, case_insensitive=True)
client = discord.Client()

# AIML startup
kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")


# on_ready
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, 
        activity = discord.Activity(type = discord.ActivityType.listening, name=";help"))
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

    print('---------------')
    print("Logged in as : ")
    print(client.user.name)
    print(client.user.id)
    print("---------------")

# on_message
@composed(client.event, with_goto)
#@with_goto
async def on_message(message):

    #-----------------------------------------------------------------#
    def food_embed1(column):
        embed.add_field(name="Measure", value=column[1])
        embed.add_field(name="Grams", value=column[2])
        embed.add_field(name="Calories", value=column[3])
        embed.add_field(name="Protein", value=column[4])
        embed.add_field(name="Fat", value=column[5])
        embed.add_field(name="Sat.Fat", value=column[6])
        embed.add_field(name="Fiber", value=column[7])
        embed.add_field(name="Carbs", value=column[8])
        embed.add_field(name="Category", value=column[9])
        embed.add_field(name="Note -", value="0 ~ miniscule amount.")

    def food_embed2(column):
        embed.add_field(name="Energy", value=column[1]+" kcal/kJ")
        embed.add_field(name="Water", value=column[2]+" g")
        embed.add_field(name="Protein", value=column[3]+" g")
        embed.add_field(name="Total Fat", value=column[4]+" g")
        embed.add_field(name="Carbohydrates", value=column[5]+" g")
        embed.add_field(name="Fiber", value=column[6]+" g")
        embed.add_field(name="Sugars", value=column[7]+" mg")
        embed.add_field(name="Calcium", value=column[8]+" mg")
        embed.add_field(name="Iron", value=column[9]+" mg")
        embed.add_field(name="Magnessium", value=column[10]+" mg")
        embed.add_field(name="Phosphorous", value=column[11]+" g")
        embed.add_field(name="Potassium", value=column[12]+" mg")
        embed.add_field(name="Sodium", value=column[13]+" g")
        embed.add_field(name="Vitamin A", value=column[14]+" IU")
        embed.add_field(name="Vitamin C", value=column[15]+" mg")
        embed.add_field(name="Vitamin B1", value=column[16]+" mg")
        embed.add_field(name="Vitamin B2", value=column[17]+" mg")
        embed.add_field(name="Vitamin B3", value=column[18]+" mg")
        embed.add_field(name="Vitamin B5", value=column[19]+" mg")
        embed.add_field(name="Vitamin B6", value=column[20]+" mg")
        embed.add_field(name="Vitamin E", value=column[21]+" mg")

    def food_embed3(column):
        embed.add_field(name="Manufacturer", value=column[1])
        embed.add_field(name="Type", value=column[2])
        embed.add_field(name="Calories", value=column[3])
        embed.add_field(name="Protein", value=column[4])
        embed.add_field(name="Fat", value=column[5])
        embed.add_field(name="Sodium", value=column[6])
        embed.add_field(name="Fiber", value=column[7])
        embed.add_field(name="Carbohydrates", value=column[8])
        embed.add_field(name="Sugar", value=column[9])
        embed.add_field(name="Potassium", value=column[10])
        embed.add_field(name="Vitamins", value=column[11])
        embed.add_field(name="Shelf", value=column[12])
        embed.add_field(name="Weight", value=column[13])
        embed.add_field(name="Cups", value=column[14])

    def help_embed():
        embed.add_field(name=";help", value="Type ;help to get the list of commands")

    #-----------------------------------------------------------------#

    channel = message.channel
    
    if message.author.bot or str(message.channel) != channel_name:
        return
    
    if message.author == client.user:
        return

    if message.content is None:
        return

    if "https://" in message.content.lower() or "www." in message.content.lower():
        return

    if message.content == "<>":
        msg = "> Yo, I'm " + client.user.name + ".\nType `;help` for more info"
        await channel.send(msg.format(message))
        return

    elif message.content.lower() == ";help":
        embed = discord.Embed(title="Help", description="List of commands", colour=colour)
        embed.add_field(name=";info", value="Shows information about the bot.")
        embed.add_field(name=";invite", value="Server invitation link.")
        embed.add_field(name=";food-value", value="Get to know the nutritional value of the food items.")
        embed.add_field(name=";bmi", value="Get to know the BMI command.")
        embed.add_field(name=";suggest-diet", value="Want to get a suitable diet for yourself? Type in the command to know more.")        
        await channel.send(embed=embed)

    elif message.content.lower() == ";info":
        msg = "About me?\n>>> Yo, I'm " + client.user.name + ", a nutritionist chatbot.\nI love cooking, baking cakes and cleaning.\nType `;help` for more info"
        await channel.send(msg.format(message))

    elif message.content.lower() == ";invite":
        msg = "Invite your friends to \"" + server_name + "\" server!\nInvite Link : "+ invite_link+"\nType `;help` for more info"
        await channel.send(msg.format(message))

    elif message.content.lower() == ";food-value":
        embed = discord.Embed(title="Food value", description="Get to know the nutritional value of the food items.", colour=colour)
        embed.add_field(name="!food-value", value="Enter the food name after \"!food-value\" to get the details!\neg : !food-value avocado")
        help_embed()
        await channel.send(embed=embed)

    elif message.content.lower() == ";bmi":
        embed = discord.Embed(title="Body Mass Index(BMI)", description="Body Mass Index (BMI) is a person's weight in kilograms divided by the square of height in meters. A high BMI can be an indicator of high body fatness. BMI can be used to screen for weight categories that may lead to health problems but it is not diagnostic of the body fatness or health of an individual.", colour=colour)
        embed.add_field(name="!bmi", 
            value="Enter your weight(in kg) and height(in metres) after\"!bmi\"\n to calculate your BMI!\neg : Suppose you weigh 55 kg and are 1.63 m tall. Enter :\n!bmi 55 1.63")
        embed.add_field(name="Disclaimer", 
            value="BMI is not used for muscle builders, long distance athletes, pregnant women, the elderly or young children.")
        help_embed()
        await channel.send(embed=embed)

    elif message.content.lower() == ";suggest-diet":
        embed = discord.Embed(title="Diet suggestion", description="Find a suitable diet for yourself.", colour=colour)
        embed.add_field(name="!suggest-diet", 
            value="To get yourself a diet, you would be required to choose a combination of numbers.\n\nGender :\n1. Male\n2. Female\n\nWeight (in kg) : <input your weight>\n\nHeight (in cm) : <input your height>\n\nAge (in years) : <input your age>\n\nExercise :\n1. Sedentary (little or no exercise)\n2. Lightly active (1-3 days/week)\n3. Moderately active (3-5 days/week)\n4. Very active (6-7 days/week)\n5. Super active (Twice/day)\n\nFor input steps, read below.")
        help_embed()
        await channel.send(embed=embed)
        msg1 = "```Suppose you are a MALE(1), with weight 55 kg, 163 cm height, and an age of 20 years with SEDENTARY exercise plan(1).\n\nThen type command !suggest-diet 1 55 163 20 1```"
        msg2 = "```Suppose you are a FEMALE(2), with weight 67 kg, 174 cm height, and an age of 28 years with MODERATELY ACTIVE exercise plan(3).\n\nThen type command !suggest-diet 2 67 174 28 3```"
        msg3 = "```Disclaimer :\nThe suggested diet would not take into account any acute, chronic, genetic or any other types of diseases or allergies, and is strongly suggested for a person(s) with no such history. ```"
        await channel.send(msg1.format(message))
        await channel.send(msg2.format(message))
        await channel.send(msg3.format(message))

    elif re.match("^!food-value", message.content):
        food_string = " ".join((message.content).split())
        food_name = food_string[12:]
        a1,a2,a3,a4 = 0,0,0,0
        if food_name != "":
            embed = discord.Embed(title=food_name, description="", colour=colour)

            csv_file1 = csv.reader(open('kaggle\\01_nutrients_csvfile.csv', "r"), delimiter=",")
            for row1 in csv_file1:
                for column1 in csv_file1:
                    if(similar(food_name.lower(), column1[0].lower()) == 1.0):
                        a1 += 1
                        food_embed1(column1)
                        break
                break
                goto .end

            if(a1==0):
                csv_file2 = csv.reader(open('kaggle\\02_vegetables.csv', "r"), delimiter=",")
                for row2 in csv_file2:
                    for column2 in csv_file2:
                        if(similar(food_name.lower(), column2[0].lower()) == 1.0):
                            a2 += 1
                            food_embed2(column2)
                            break
                    break
                    goto .end

            if(a1==0 and a2==0):
                csv_file3 = csv.reader(open('kaggle\\03_fruits.csv', "r"), delimiter=",")
                for row3 in csv_file3:
                    for column3 in csv_file3:
                        if(similar(food_name.lower(), column3[0].lower()) == 1.0):
                            a3 += 1
                            food_embed2(column3)
                            break
                    break
                    goto .end

            if(a1==0 and a2==0 and a3==0):
                csv_file4 = csv.reader(open('kaggle\\04_cereal.csv', "r"), delimiter=",")
                for row4 in csv_file4:
                    for column4 in csv_file4:
                        if(similar(food_name.lower(), column4[0].lower()) == 1.0):
                            a4 += 1
                            food_embed3(column4)
                            break
                    break
                    goto .end

        if(a1==0):
            b1=0
            csv_file1 = csv.reader(open('kaggle\\01_nutrients_csvfile.csv', "r"), delimiter=",")
            for row1 in csv_file1:
                for column1 in csv_file1:
                    if(0.65 < similar(food_name.lower(), column1[0].lower()) < 1.0):
                        b1 += 1
                        embed.add_field(name="Did you mean?", value=column1[0])
        if(a2==0):
            b2=0
            csv_file2 = csv.reader(open('kaggle\\02_vegetables.csv', "r"), delimiter=",")
            for row2 in csv_file2:
                for column2 in csv_file2:
                    if(0.65 < similar(food_name.lower(), column2[0].lower()) < 1.0):
                        b2 += 1
                        embed.add_field(name="Did you mean?", value=column2[0])
        if(a3==0):
            b3=0
            csv_file3 = csv.reader(open('kaggle\\03_fruits.csv', "r"), delimiter=",")
            for row3 in csv_file3:
                for column3 in csv_file3:
                    if(0.65 < similar(food_name.lower(), column3[0].lower()) < 1.0):
                        b3 += 1
                        embed.add_field(name="Did you mean?", value=column3[0])
        if(a4==0):
            b4=0
            csv_file4 = csv.reader(open('kaggle\\04_cereal.csv', "r"), delimiter=",")
            for row4 in csv_file4:
                for column4 in csv_file4:
                    if(0.65 < similar(food_name.lower(), column4[0].lower()) < 1.0):
                        b4 += 1
                        embed.add_field(name="Did you mean?", value=column4[0])   

        if(a1==0 and a2==0 and a3==0 and a4==0 and b1==0 and b2==0 and b3==0 and b4==0):
            embed.add_field(name="Note -", value="If no results are returned then the search query doesn't exist in database :(")
            goto .end

        label .end
        help_embed()
        await channel.send(embed=embed)

    elif re.match("^!bmi", message.content):  
        bmi_string = " ".join((message.content).split())
        bmi_input = bmi_string[5:]
        x = bmi_input.split()
        if(len(x) == 2):
            if(isFloat(x[0]) and isFloat(x[1])):
                w = float(x[0])
                h = float(x[1])
                if(w > 0 and h > 0):
                    bmi_val = w/(h*h)
                    bmi_val = "{:.2f}".format(round(bmi_val, 2))
                    bmi_val = float(bmi_val)
                    embed = discord.Embed(title="Body Mass Index (BMI)", description=str(bmi_val), colour=colour)
                
                    if(bmi_val < 18.5):
                        embed.add_field(name="Underweight", value="Your BMI value is less than 18.5. Unhealthy BMI.")
                        embed.add_field(name="Symptoms", value="-> Osteoporosis\n-> Skin, hair, or teeth problems\n-> Getting sick frequently\n-> Feeling tired all the time\n-> Anemia\n-> Irregular periods(for women)\n-> Premature births(for women)\n-> Slow or impaired growth(for young kids)")
                        embed.add_field(name="Causes", value="-> Family history\n-> High metabolism\n-> Frequent physical activity\n-> Physical illness or chronic disease\n-> Mental illness")
                        embed.add_field(name="Treatment", value="-> High-protein and whole-grain carbohydrate snacks\n-> Eating several small meals a day\n-> Incorporating additional foods\n-> Avoid foods that are high in sugar and salt")
                
                    elif(18.5 <= bmi_val <= 24.9):
                        embed.add_field(name="Normal/Healthy", value="Your BMI value lies between 18.5 and 24.9. Healthy BMI.")
                        embed.add_field(name="Tips", value="You are at a healthy weight for your height. By maintaining a healthy weight, you lower your risk of developing serious health problems.")
                
                    elif(25 <= bmi_val <= 29.9):
                        embed.add_field(name="Overweight", value="Your BMI value lies between 25 and 29.9. Unhealthy BMI.")
                        embed.add_field(name="Tips", value="Overweight BMI isn't necessarily bad. Make sure to avoid eating foods that provide excessive fats. Increase your physical activity.")
                        
                    else:
                        embed.add_field(name="Obese", value="Your BMI value is greater than 29.9. Unhealthy BMI.")
                        embed.add_field(name="Causes", value="-> Intake of excessive calories than required\n-> Family inheritance and influences\n-> Lifestyle choices(Unhealthy diet, Liquid calories, Inactivity)")
                        embed.add_field(name="Treatment", value="-> Dietary changes\n-> Increased physical activity\n-> Behavior changes\n-> Prescription medications(Optional)\n-> Weight-loss procedures(Optional)")
                        embed.add_field(name="Prevention", value="-> Exercise regularly\n-> Follow a healthy-eating plan\n-> Know and avoid the food traps that cause you to eat\n-> Monitor your weight regularly\n-> Be consistent with your health plans")

                    help_embed()
                    await channel.send(embed=embed)
                else:
                    await channel.send("**Invalid input** - Weight and height must be a positive number.")
            else:
                await channel.send("**Invalid input** - Must be a number.")
        else:
            await channel.send("**Invalid input** - Must have 2 values. You are missing on something.")

    elif re.match("^!suggest-diet", message.content):
        diet_string = " ".join((message.content).split())
        diet_input = diet_string[14:]
        x = diet_input.split()
        if(len(x) == 5):
            if(isInt(x[0]) and isFloat(x[1]) and isFloat(x[2]) and isFloat(x[3]) and isInt(x[4])):
                w = float(x[1])
                #w = w * 2.20462
                h = float(x[2])
                #h = h * 
                age = float(x[3])

                if(w>0 and h>0 and age>0):
                    if(x[0] == "1"):
                        #gender = "male"
                        #cal = 88.362 + (13.397*w) + (4.799*h) - (5.677*age)
                        #cal = 10*w + 6.25*h - 5*age + 5
                        cal = 66.5 + (13.75 * w) + (5.003 * h) - (6.755 * age)
                    elif(x[0] == "2"):
                        #gender = "female"
                        #cal = 447.593 + (9.247*w) + (3.098*h) - (4.330*age)
                        #cal = 10*w + 6.25*h - 5*age - 161
                        cal = 655 + (9.563 * w) + (1.850 * h) - (4.676 * age)
                    else:
                        await channel.send("**Invalid input** - Invalid input for gender. Must be 1 or 2.")
                        
                    if(1 <= int(x[4]) <=5):
                        act = x[4]
                    else:
                        await channel.send("**Invalid input** - Invalid input for exercise plan. Must be from set {1, 2, 3, 4, 5}.")

                    if(act == "1"): #Sedentary (little or no exercise)
                        cal = cal*1.2
                    elif(act == "2"): #Lightly active (1-3 days/week)
                        cal = cal*1.375
                    elif(act == "3"): #Moderately active (3-5 days/week)
                        cal = cal*1.55
                    elif(act == "4"): #Very active (6-7 days/week)
                        cal = cal*1.725
                    elif(act == "5"): #Super active (twice/day)
                        cal = cal*1.9

                    protein = ['Yogurt(1 cup)','Cooked meat(3 Oz)','Cooked fish(4 Oz)','1 whole egg','4 egg whites','Tofu(5 Oz)']
                    fruit = ['Berries(80 Oz)','Apple','Orange','Banana','Dried Fruits(Handful)','Fruit Juice(125ml)']
                    vegetable = ['Any vegetable(80g)']
                    grains = ['Cooked Grain(150g)','Whole Grain Bread(1 slice)','Half Large Potato(75g)','Oats(250g)','2 corn tortillas']
                    ps = ['Soy nuts(i Oz)','Low fat milk(250ml)','Hummus(4 Tbsp)','Cottage cheese (125g)','Flavored yogurt(125g)']
                    taste_en = ['2 TSP (10 ml) olive oil','2 TBSP (30g) reduced-calorie salad dressin','1/4 medium avocado','Small handful of nuts','1/2 ounce  grated Parmesan cheese','1 TBSP (20g) jam, jelly, honey, syrup, sugar']

                    #embed = discord.Embed(title="Recommended diet", description="Your daily calorie intake is around "+"{:.2f}".format(round(bmi_val, 2))+" Kcal/day.", colour=colour)
                    if cal<1500:
                        msg = "```Your daily calorie intake is around "+"{:.2f}".format(round(cal, 2))+" Kcal/day.\n\nRecommended diet :\nBreakfast : "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+"\nLunch : "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+"\nSnack : "+ps[randint(0, 4)]+" + "+vegetable[0]+"\nDinner : "+protein[randint(0, 5)]+" + 2 × "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+"\nSnack : "+fruit[randint(0, 5)]+"```"
                        await channel.send(msg.format(message))
                        """
                        embed.add_field(name="Breakfast", value=protein[randint(0, 5)]+" + "+fruit[randint(0, 5)])
                        embed.add_field(name="Lunch", value=protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)])
                        embed.add_field(name="Snack", value=ps[randint(0, 4)]+" + "+vegetable[0])
                        embed.add_field(name="Dinner", value=protein[randint(0, 5)]+" + 2 "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)])
                        embed.add_field(name="Snack", value=fruit[randint(0, 5)])                 
                        await channel.send(embed=embed)
                        """

                    elif cal<1800:
                        msg = "```Your daily calorie intake is around "+"{:.2f}".format(round(cal, 2))+" Kcal/day.\n\nRecommended diet :\nBreakfast : "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+"\nLunch : "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)]+"\nSnack : "+ps[randint(0, 4)]+" + "+vegetable[0]+"\nDinner : "+"2 × "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+"\nSnack : "+fruit[randint(0, 5)]+"```"
                        await channel.send(msg.format(message))
                        """
                        embed.add_field(name="Breakfast", value=protein[randint(0, 5)]+" + "+fruit[randint(0, 5)])
                        embed.add_field(name="Lunch", value=protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)])
                        embed.add_field(name="Snack", value=ps[randint(0, 4)]+" + "+vegetable[0])
                        embed.add_field(name="Dinner", value="2 "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)])
                        embed.add_field(name="Snack", value=fruit[randint(0, 5)])                    
                        await channel.send(embed=embed)
                        """

                    elif cal<2200:
                        msg = "```Your daily calorie intake is around "+"{:.2f}".format(round(cal, 2))+" Kcal/day.\n\nRecommended diet :\nBreakfast : "+"2 × "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+" + "+grains[randint(0,4)]+"\nLunch : "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)]+"\nSnack : "+ps[randint(0, 4)]+" + "+vegetable[0]+"\nDinner : "+"2 × "+protein[randint(0, 5)]+" + 2 × "+vegetable[0]+" + Leafy Greens + 2 × "+grains[randint(0,4)]+" + 2 × "+taste_en[randint(0,5)]+"\nSnack : "+fruit[randint(0, 5)]+"```"
                        await channel.send(msg.format(message))
                        """
                        embed.add_field(name="Breakfast", value="2 "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+" + "+grains[randint(0,4)])
                        embed.add_field(name="Lunch", value=protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)])
                        embed.add_field(name="Snack", value=ps[randint(0, 4)]+" + "+vegetable[0])
                        embed.add_field(name="Dinner", value="2 "+protein[randint(0, 5)]+" + 2 "+vegetable[0]+" + Leafy Greens + 2 "+grains[randint(0,4)]+" + 2 "+taste_en[randint(0,5)])
                        embed.add_field(name="Snack", value=fruit[randint(0, 5)])                      
                        await channel.send(embed=embed)
                        """

                    elif cal>=2200:
                        msg = "```Your daily calorie intake is around "+"{:.2f}".format(round(cal, 2))+" Kcal/day.\n\nRecommended diet :\nBreakfast : "+"2 × "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+" + "+grains[randint(0,4)]+"\nLunch : "+protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens + "+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)]+"\nSnack : "+ps[randint(0, 4)]+" + "+vegetable[0]+"\nDinner : "+"2 × "+protein[randint(0, 5)]+" + 2 × "+vegetable[0]+" + Leafy Greens + 2 × "+grains[randint(0,4)]+" + 2 × "+taste_en[randint(0,5)]+"\nSnack : "+fruit[randint(0, 5)]+"```"
                        await channel.send(msg.format(message))
                        """
                        embed.add_field(name="Breakfast", value="2 "+protein[randint(0, 5)]+" + "+fruit[randint(0, 5)]+" + "+grains[randint(0,4)])
                        embed.add_field(name="Lunch", value=protein[randint(0, 5)]+" + "+vegetable[0]+" + Leafy Greens"+grains[randint(0,4)]+" + "+taste_en[randint(0,5)]+" + "+fruit[randint(0, 5)])
                        embed.add_field(name="Snack", value=ps[randint(0, 4)]+" + "+vegetable[0])
                        embed.add_field(name="Dinner", value="2 "+protein[randint(0, 5)]+" + 2 "+vegetable[0]+" + Leafy Greens + 2 "+grains[randint(0,4)]+" + 2 "+taste_en[randint(0,5)])
                        embed.add_field(name="Snack", value=fruit[randint(0, 5)])                      
                        await channel.send(embed=embed)
                        """


                else:
                    await channel.send("**Invalid input** - Age, weight and height be positive numbers.")
            else:
                await channel.send("**Invalid input** -\n1. All inputs should be numbers.\n2. Gender should be represented as 1 or 2; \"1\" being male and \"2\" being female.\n3. Age should be in years.\n4. Height and weight can be in decimals.\n5. Exercise plan should be from set {1, 2, 3, 4, 5}.")
        else:
            await channel.send("**Invalid input** - Must have 5 values. You are missing on something.")

        """
        if(len(x) == 2):
            if(RepresentsFloat(x[0]) and RepresentsFloat(x[1])):
                w = float(x[0])
                h = float(x[1])
        """

    else:
        response = kernel.respond(message.content)
        await asyncio.sleep(random.randint(0,2))
        await channel.send(response.format(message))





client.run(TOKEN)
