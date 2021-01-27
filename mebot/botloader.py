import aiml
import os


# ----
# constants
BOT_DIR_PATH = "./mebot/"
BOT_BRAIN = "mebot.brn"
# in dev enviornment we make brain on each run because .aiml files might have been edited
ENV = os.getenv("MEBOT_ENV", "PROD")  # default val is PROD
# ----

# ----
# predicates
bot_predicates = {"name": "mebot", "version": "1.0", "botmaster": "Haider"}
# ----


def create_brain(k):
    for file in os.listdir(BOT_DIR_PATH):
        fullpath = BOT_DIR_PATH + file
        # load only .aiml files
        if fullpath.endswith(".aiml"):
            k.learn(fullpath)

    k.saveBrain(BOT_BRAIN)


def init(k):
    if ENV == "DEV" or not os.path.isfile(BOT_BRAIN):
        pass
    create_brain(k)
    k.bootstrap(brainFile=BOT_BRAIN)
    # setup bot (global) predicates
    for kv in bot_predicates.items():
        k.setBotPredicate(*kv)
