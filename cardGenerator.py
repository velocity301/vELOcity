import matplotlib as plt
from PIL import Image, ImageFont, ImageDraw
# # Drawing an image on another image
# baseImage = Image.open("PlayerCards/PlayerCard.png")
# overlayImage = Image.open("PlayerCards/elo.png")
# result = Image.new("RGBA", baseImage.size)
# result.paste(baseImage, (0,0))
# result.paste(overlayImage, (50,50), overlayImage)
# result.save("PlayerCards/result.png")

# Draws overlayText on a baseImage
def drawTextElement(baseImage, overlayText, maxWidth, maxHeight, textPositionX, textPositionY, outputFile):
    img = Image.open(f"PlayerCards/{baseImage}")
    draw = ImageDraw.Draw(img)
    text = overlayText
    fontSize = 200
    font = ImageFont.truetype("PlayerCards/VALORANT.ttf", fontSize)
    textWidth, textHeight = draw.textsize(text, font=font)
    while(textWidth > maxWidth or textHeight > maxHeight):
        fontSize -= 1
        font = ImageFont.truetype("PlayerCards/VALORANT.ttf", fontSize)
        textWidth, textHeight = draw.textsize(text, font=font)
    textPosition = (textPositionX, textPositionY) #(580, 150)
    print(overlayText)
    print(fontSize)
    draw.text((textPositionX-textWidth/2, textPositionY-textHeight/2), text, font=font, fill=(0, 0, 0))
    img.save(f"PlayerCards/{outputFile}") 


# Creating Spider Chart
import matplotlib.pyplot as plt
import numpy as np

# # create the categories and values
# categories = ['category 1', 'category 2', 'category 3', 'category 4', 'category 5']
# values = [3, 5, 2, 4, 1]

# # create the spider char t
# ax = plt.subplot(111, polar=True)
# ax.set_theta_zero_location('N')
# ax.set_theta_direction(-1)
# ax.set_ylim(0, 6)
# ax.set_yticks(np.arange(1, 6))
# ax.set_yticklabels([])
# ax.set_xticks(np.linspace(0, 2*np.pi, len(categories), endpoint=False))
# ax.set_xticklabels(categories)
# ax.plot(np.linspace(0, 2*np.pi, len(categories), endpoint=False), values)
# ax.fill(np.linspace(0, 2*np.pi, len(categories), endpoint=False), values, 'b', alpha=0.1)
# # show the chart
# plt.show()

def generateCard(discordName, valorantName, rank, ELO, winPercentage, 
headShotPercentage, averageDamagePerRound, firstBloodPercentage, clutchPercentage, assistsPerRound):
    # grab background art relevant to most played agent
    # overlay basic card template
    # place valorantName.split("#")[0]
    drawTextElement("PlayerCard.png", valorantName.split('#')[0], 500, 100, 580, 150, "working.png")
    # place discordName
    drawTextElement("working.png", discordName, 500, 50, 430, 328, "working.png")
    # place valorantName
    drawTextElement("working.png", valorantName, 500, 50, 430, 448, "working.png")
    # place ELO
    if ELO < 1000:
        drawTextElement("working.png", "Rating:" + str(ELO), 400, 300, 755, 1170, "working.png")
    elif ELO >= 1000:
        drawTextElement("working.png", "Rating:" + str(ELO), 400, 300, 750, 1170, "working.png")
    # find win percentage
    # find headShotPercentage
    # find averageDamagePerRound
    # find firstBloodPercentage
    # find clutchPercentage
    # find assistsPerRound
    # place titles
    
    # place overall score
    drawTextElement("working.png", str(99), 300, 300, 860, 1530, "working.png")

generateCard("Velocity#9534", "Velocity#300", "Platinum", 1200, 55.3, 22.2, 132.2, 8.1, 22.1, 1.4)