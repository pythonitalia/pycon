from wagtail import blocks


class BackgroundColorChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ("coral", "coral"),
        ("caramel", "caramel"),
        ("cream", "cream"),
        ("yellow", "yellow"),
        ("green", "green"),
        ("purple", "purple"),
        ("pink", "pink"),
        ("blue", "blue"),
        ("red", "red"),
        ("success", "success"),
        ("warning", "warning"),
        ("neutral", "neutral"),
        ("error", "error"),
        ("black", "black"),
        ("grey", "grey"),
        ("white", "white"),
        ("milk", "milk"),
    ]

    class Meta:
        icon = "crosshairs"


class IllustrationChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ("cathedral", "Cathedral"),
        ("florence", "Florence"),
        ("florence2", "Florence2"),
        ("handWithSnakeInside", "Hand With Snake Inside"),
        ("snake1", "Snake1"),
        ("snake2", "Snake2"),
        ("snake4", "Snake4"),
        ("snake5", "Snake5"),
        ("snakeBody", "Snake Body"),
        ("snakeCouple", "Snake Couple"),
        ("snakeDNA", "Snake D N A"),
        ("snakeHead", "Snake Head"),
        ("snakeInDragon", "Snake In Dragon"),
        ("snakeInDragonInverted", "Snake In Dragon Inverted"),
        ("snakeLetter", "Snake Letter"),
        ("snakeLongNeck", "Snake Long Neck"),
        ("snakePencil", "Snake Pencil"),
        ("snakeTail", "Snake Tail"),
        ("snakeWithBalloon", "Snake With Balloon"),
        ("snakeWithContacts", "Snake With Contacts"),
        ("snakesWithBanner", "Snakes With Banner"),
        ("snakesWithCocktail", "Snakes With Cocktail"),
        ("snakesWithDirections", "Snakes With Directions"),
        ("snakesWithOutlines", "Snakes With Outlines"),
        ("tripleSnakes", "Triple Snakes"),
    ]

    class Meta:
        icon = "image"
