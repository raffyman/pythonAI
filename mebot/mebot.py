from datetime import datetime
from py2neo import Graph, NodeMatcher
from py2neo.data import Node
import aiml
import botloader
import colorful as cf
import graph
import os
import parser
import random
import respond

cf.use_style("solarized")

# ----
# constants
BOT_DIR_PATH = "./mebot/"
BOT_BRAIN = "mebot.brn"
ENV = os.getenv("MEBOT_ENV", "PROD")  # default val is PROD
# ----


class MeBot:
    def __init__(self, user_ip=""):

        # variables
        self.user_ip = user_ip
        self.k = aiml.Kernel()
        botloader.init(self.k)

        # bot states
        self.is_login = False
        self.user_check = False
        self.user_exists = False
        self.ask_pass = False

        # for new users
        self.ask_name = False
        self.ask_username = False
        self.ask_pass = False

        self.matcher = graph.get_nodematcher_instance()
        self.graphi = graph.get_graph_instance()

        # init the responder
        respond.init(self.k)

    def login(self, msg):
        # the message is here

        if not self.user_check:
            # search user in the DB
            person = self.matcher.match("Person", ip=self.user_ip).first()
            if person:
                self.user_exists = True
            self.user_check = False  # this if block will only run this one time

        if self.user_exists:
            self.k.setPredicate("name", person.get("name"))
            self.k.setPredicate("username", person.get("username"))
            password = person.get("password")
            # self.k.setPredicate("pass", person.get("password"))
            self.k.setPredicate("met_on", person.get("met_on"))

            if not self.ask_pass:
                self.ask_pass = True
                return (
                    "Hey! I know you %s! But you must tell me your password first."
                    % self.k.getPredicate("name")
                )

            self.k.respond(msg)  # so predicate can be set
            if str(password) != str(self.k.getPredicate("pass")):
                return "INVALID PASSWORD"
            else:
                self.is_login = True
                return "Welcome back!"
        else:
            self.k.respond(msg)  # so predicates can be set

            if not self.ask_name:
                print(cf.yellow("name"), self.k.getPredicate("name"))
                if not self.k.getPredicate("name"):
                    return "Please tell me your name"
                else:
                    self.ask_name = True

            if not self.ask_username:
                if not self.k.getPredicate("username"):
                    return "Please tell me your username"
                else:
                    self.ask_username = True

            if not self.ask_pass:
                if not self.k.getPredicate("pass"):
                    return (
                        "Please tell me your password. Don't worry, I won't tell anyone"
                    )
                else:
                    self.ask_pass = True

            if (
                self.k.getPredicate("name")
                and self.k.getPredicate("username")
                and self.k.getPredicate("pass")
            ):
                person = Node(
                    "Person",
                    name=self.k.getPredicate("name"),
                    username=self.k.getPredicate("username"),
                    password=self.k.getPredicate("pass"),
                    ip=self.user_ip,
                    met_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                self.graphi.create(person)

                if ENV == "DEV":
                    print("[DEV] name=", self.k.getPredicate("name"))
                    print("[DEV] username=", self.k.getPredicate("username"))
                    print("[DEV] pass=", self.k.getPredicate("pass"))
                    print("[DEV] ip=", self.user_ip)

            self.is_login = True
            return "Welcome!"

    def conversate(self, msg):
        if self.is_login:
            user = {"ip": self.user_ip}
            try:
                # pass
                strc, ncs = parser.parser(msg)
                parser.embed_types(strc, ncs)
                graph.make_graph(strc, ncs, clear=False, user=user)

                return random.choice(
                    ["I see.", "Interesting.", "Oh, I didn't know that"]
                )
            except:
                print("error")
                pass

            return respond.reply(msg, user=user)
        else:
            # try to log them in first
            return self.login(msg)
