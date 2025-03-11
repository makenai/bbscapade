#!/usr/bin/env python3
"""
BBScapade - An AI-powered BBS nostalgia experience
"""

import os
import time
import random
import sys
from typing import Dict, List, Any
import signal

# Third-party libraries
import anthropic
from colorama import init, Fore, Back, Style
import pyfiglet
import simpleaudio as sa
from dotenv import load_dotenv
import requests

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    print(f"{Fore.RED}Error: CLAUDE_API_KEY not found in environment variables.")
    print(f"{Fore.YELLOW}Please create a .env file with your API key or set it in your environment.")
    sys.exit(1)

# Initialize Claude client
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

class BBScapade:
    def __init__(self):
        self.client = claude
        self.logged_in = False
        self.user_name = ""
        self.current_board = "Main"
        self.messages = []
        
    def play_dialup_sound(self):
        """Play the classic dialup modem sound"""
        try:
            # Use afplay to play the sound file at 2x speed
            os.system('afplay -r 2 assets/dialup.wav &')

            # Display "Connecting..." while the sound plays
            self._slow_print(f"{Fore.CYAN}Connecting to BBS", end="")
            for _ in range(10):
                time.sleep(1.2)
                print(f"{Fore.CYAN}.", end="", flush=True)
            print()
            
        except FileNotFoundError:
            print(f"{Fore.YELLOW}Warning: Dialup sound file not found. Continuing without sound.")
            time.sleep(2)

    def display_welcome_screen(self):
        """Display the welcome ASCII art and info"""
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Generate random BBS name and tagline from Claude
        bbs_info = self._generate_bbs_info()
        
        # Get a random font for the BBS name
        fonts = ['slant', 'banner', 'big', 'block', 'bubble', 'digital', 'ivrit', 
                'mini', 'script', 'shadow', 'small', 'smscript', 'standard']
        font = random.choice(fonts)
        
        # Get random colors for different elements
        colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED, Fore.BLUE, Fore.WHITE]
        name_color = random.choice(colors)
        tagline_color = random.choice(colors)
        border_color = random.choice(colors)
        info_label_color = random.choice(colors)
        info_value_color = random.choice(colors)
        
        # Display BBS name with random font
        try:
            figlet_text = pyfiglet.figlet_format(bbs_info["name"], font=font)
        except Exception:
            # Fallback to standard font if the chosen one fails
            figlet_text = pyfiglet.figlet_format(bbs_info["name"], font="standard")
            
        print(f"{name_color}{figlet_text}")
        
        # Randomly decide whether to use the API tagline or generate a new one
        if random.random() < 0.4:  # 40% chance to use a local tagline
            # List of retro BBS-style taglines
            taglines = [
                "Where Reality Takes a Coffee Break!",
                "Uploading Weirdness Since 198X",
                "All Your Bandwidth Are Belong To Us",
                "The Digital Playground for Keyboard Cowboys",
                "Dial In, Tune Out, Drop Packets",
                "Serving Internet Weirdness at 2400 Baud",
                "Where Electrons Go to Party!",
                "Your Computer's Favorite Hangout",
                "Faster Than a 14.4k Modem!",
                "The Information Superhighway's Best Rest Stop",
                "Bringing Digital Dreams to Digital Screens",
                "Press Any Key to Continue... ANY Key!",
                "No Carrier? No Problem!",
                "Loading Nostalgia... Please Wait...",
                "Where Text is King and Graphics are Optional",
                "Breaking the Internet Before It Was Cool",
                "Packet Loss is Just Part of the Experience",
                "Keeping Modems Warm Since the 80s",
                "Connecting Digital Souls at the Speed of Light",
                "The Place Where Time Stands Still at 9600 Baud"
            ]
            bbs_info['tagline'] = random.choice(taglines)
        
        # Display tagline
        print(f"{tagline_color}{Style.BRIGHT}{bbs_info['tagline']}{Style.RESET_ALL}")
        print(f"{border_color}{'=' * 60}")
        
        # Display sysop info
        print(f"{info_label_color}SysOp: {info_value_color}{bbs_info['sysop']}")
        print(f"{info_label_color}Established: {info_value_color}{bbs_info['established']}")
        print(f"{info_label_color}Node Count: {info_value_color}{bbs_info['nodes']}")
        print(f"{border_color}{'=' * 60}")
        
        # Random ASCII art chance (25%)
        if random.random() < 0.25:
            ascii_arts = [
                r"""
                 ______________
                /             /|
                /____________/ |
                |  _______  |  |
                | |       | |  |
                | |_______| | /
                |___________|/
                """,
                r"""
                 .---.
                /_____\
                ( '.' )
                 \_-_/_
                .-"`'`"-.
                /________\
                """,
                r"""
                 ________
                /  cO Od \
                |   xxx   |
                \   --   /
                 \______/
                """,
                r"""
                 _______
                |.-----.|
                ||x . x||
                ||_.-._||
                `--)-(--`
                /__/_\__\
                """,
                r"""
                   _
                  [_]
                 /|_|\
                (/ \ \)
                """,
            ]
            print(f"{random.choice(colors)}{random.choice(ascii_arts)}")
        
        print(f"{Fore.CYAN}Welcome to this unique BBS experience!")
        print(f"{Fore.CYAN}Each time you connect, a new randomly generated BBS awaits...")
        print()

    def _generate_bbs_info(self) -> Dict[str, Any]:
        """Generate a random, weird, and funny BBS info using Claude"""
        import json
        import re
        import time
        import random

        # Maximum number of retry attempts
        max_retries = 3
        # Initial delay between retries (in seconds)
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Make the API call to Claude
                message = claude.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    temperature=1.0,
                    system="You are generating content for a nostalgic BBS simulation. Create weird, absurd, and hilarious BBS details. Be creative, funny, and strange but keep it appropriate.",
                    messages=[
                        {
                            "role": "user",
                            "content": "Generate a JSON-like structure for a fictional BBS with the following fields: name (short name, max 20 chars), tagline (funny/weird slogan), sysop (bizarre username), established (year between 1985-1995), nodes (number between 1-8), and a list of 3-5 bizarre board_names. Make it weird, absurd, and hilarious but appropriate. Return ONLY valid JSON."
                        }
                    ]
                )
                
                # Extract the content from Claude's response
                content = message.content[0].text
                
                # Try to find and parse JSON from the response
                # First attempt: Look for JSON structure using regex
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                
                if json_match:
                    json_str = json_match.group(0)
                    try:
                        # Parse the JSON string
                        response = json.loads(json_str)
                        
                        # Validate that all required fields are present
                        required_fields = ["name", "tagline", "sysop", "established", "nodes", "board_names"]
                        if all(field in response for field in required_fields):
                            # Make sure name isn't too long
                            if len(response["name"]) > 20:
                                response["name"] = response["name"][:20]
                            
                            # Make sure board_names is a list
                            if not isinstance(response["board_names"], list):
                                raise ValueError("board_names is not a list")
                                
                            return response
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"{Fore.YELLOW}Warning: Error parsing JSON: {e}. Retrying...")
                
                # If we get here, something went wrong with parsing
                # Wait before retrying with exponential backoff
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    print(f"{Fore.YELLOW}Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                
            except Exception as e:
                # Wait before retrying
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    print(f"{Fore.RED}API call failed: {e}. Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    print(f"{Fore.RED}API call failed after {max_retries} attempts: {e}")
        
        # If all retries failed, return fallback content
        print(f"{Fore.RED}Failed to generate BBS info after {max_retries} attempts. Using fallback content.")
        return {
            "name": "ERROR BBS",
            "tagline": "When in doubt, reboot!",
            "sysop": "SysError",
            "established": "1991",
            "nodes": "1",
            "board_names": ["Bug Reports", "System Failure", "Help Wanted"]
        }

    def login_screen(self):
        """Display the login screen and handle user authentication"""
        print(f"{Fore.GREEN}{'=' * 60}")
        print(f"{Fore.CYAN}{Style.BRIGHT}LOGIN REQUIRED{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 60}")
        
        self.user_name = input(f"{Fore.WHITE}Enter your handle: {Fore.YELLOW}")
        print(f"{Fore.CYAN}Validating user credentials...")
        time.sleep(1.5)
        
        print(f"{Fore.GREEN}Welcome aboard, {Fore.YELLOW}{self.user_name}{Fore.GREEN}!")
        self.logged_in = True
        time.sleep(1)

    def main_menu(self):
        """Display and handle the main menu"""
        while self.logged_in:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Choose a random menu style for this session
            menu_style = random.choice(["standard", "boxed", "arrow", "retro", "ascii"])
            
            # Random colors
            colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED, Fore.BLUE]
            title_color = random.choice(colors)
            option_color = random.choice([c for c in colors if c != title_color])
            number_color = random.choice([c for c in colors if c not in [title_color, option_color]])
            highlight_color = random.choice([c for c in colors if c not in [title_color, option_color, number_color]])
            
            # Display menu based on random style
            if menu_style == "standard":
                print(f"{title_color}{Style.BRIGHT}==== MAIN MENU ===={Style.RESET_ALL}")
                print(f"{number_color}1. {option_color}Message Boards")
                print(f"{number_color}2. {option_color}File Archives")
                print(f"{number_color}3. {option_color}Door Games")
                print(f"{number_color}4. {option_color}Chat with SysOp (AI)")
                print(f"{number_color}5. {option_color}Logoff")
            
            elif menu_style == "boxed":
                print(f"{title_color}╔══════════════════╗")
                print(f"{title_color}║ {Style.BRIGHT}  MAIN MENU     {Style.RESET_ALL}{title_color}║")
                print(f"{title_color}╠══════════════════╣")
                print(f"{title_color}║ {number_color}1. {option_color}Message Boards {title_color}║")
                print(f"{title_color}║ {number_color}2. {option_color}File Archives  {title_color}║")
                print(f"{title_color}║ {number_color}3. {option_color}Door Games     {title_color}║")
                print(f"{title_color}║ {number_color}4. {option_color}Chat with SysOp{title_color}║")
                print(f"{title_color}║ {number_color}5. {option_color}Logoff         {title_color}║")
                print(f"{title_color}╚══════════════════╝")
            
            elif menu_style == "arrow":
                print(f"{title_color}{Style.BRIGHT}>>> MAIN MENU <<<{Style.RESET_ALL}")
                print(f"{highlight_color}------------------")
                print(f"{number_color}1 {highlight_color}-> {option_color}Message Boards")
                print(f"{number_color}2 {highlight_color}-> {option_color}File Archives")
                print(f"{number_color}3 {highlight_color}-> {option_color}Door Games")
                print(f"{number_color}4 {highlight_color}-> {option_color}Chat with SysOp")
                print(f"{number_color}5 {highlight_color}-> {option_color}Logoff")
                print(f"{highlight_color}------------------")
            
            elif menu_style == "retro":
                print(f"{title_color}■■■■■■■■■■■■■■■■■■■■■■■■")
                print(f"{title_color}■ {Style.BRIGHT}BBS COMMAND CENTER{Style.RESET_ALL} {title_color}■")
                print(f"{title_color}■■■■■■■■■■■■■■■■■■■■■■■■")
                print(f"{option_color}  [{number_color}1{option_color}] Message Boards")
                print(f"{option_color}  [{number_color}2{option_color}] File Archives")
                print(f"{option_color}  [{number_color}3{option_color}] Door Games")
                print(f"{option_color}  [{number_color}4{option_color}] Chat with SysOp")
                print(f"{option_color}  [{number_color}5{option_color}] Logoff System")
                print(f"{title_color}■■■■■■■■■■■■■■■■■■■■■■■■")
            
            else:  # ascii
                menu_art = random.choice([
                    r"""
  /\/\   ___ _ __  _   _ 
 /    \ / _ \ '_ \| | | |
/ /\/\ \  __/ | | | |_| |
\/    \/\___|_| |_|\__,_|
                    """,
                    r"""
 __  __                  
|  \/  | ___ _ __  _   _ 
| |\/| |/ _ \ '_ \| | | |
| |  | |  __/ | | | |_| |
|_|  |_|\___|_| |_|\__,_|
                    """,
                    r"""
   ___      _   _                 
  / __\__ _| | | | ___  _ __ ___  
 / /  / _` | |_| |/ _ \| '_ ` _ \ 
/ /__| (_| |  _  | (_) | | | | | |
\____/\__,_|_| |_|\___/|_| |_| |_|
                    """
                ])
                print(f"{title_color}{menu_art}")
                print(f"{highlight_color}{'=' * 30}")
                print(f"{number_color}1. {option_color}Message Boards")
                print(f"{number_color}2. {option_color}File Archives")
                print(f"{number_color}3. {option_color}Door Games")
                print(f"{number_color}4. {option_color}Chat with SysOp")
                print(f"{number_color}5. {option_color}Logoff")
                print(f"{highlight_color}{'=' * 30}")
            
            # Get user choice with a randomized prompt
            prompts = [
                f"\n{highlight_color}Choose an option: {Fore.WHITE}",
                f"\n{highlight_color}Enter selection: {Fore.WHITE}",
                f"\n{highlight_color}Command: {Fore.WHITE}",
                f"\n{highlight_color}Your choice? {Fore.WHITE}",
                f"\n{highlight_color}What's your pleasure? {Fore.WHITE}"
            ]
            
            choice = input(random.choice(prompts))
            
            if choice == "1":
                self.message_boards()
            elif choice == "2":
                self.file_archives()
            elif choice == "3":
                self.door_games()
            elif choice == "4":
                self.chat_with_sysop()
            elif choice == "5":
                self.logoff()
                break
            else:
                print(f"{Fore.RED}Invalid option. Please try again.")
                time.sleep(1)

    def _slow_print(self, text, delay=0.03, end="\n"):
        """Print text slowly, character by character"""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print(end=end)

    def message_boards(self):
        """Display and navigate message boards"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== MESSAGE BOARDS ===={Style.RESET_ALL}")
        
        # Get BBS info to access board names
        bbs_info = self._generate_bbs_info()
        board_names = bbs_info["board_names"]
        
        # Display available boards
        print(f"{Fore.GREEN}Available message boards:\n")
        for i, board in enumerate(board_names, 1):
            print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{board}")
        print(f"{Fore.WHITE}{len(board_names) + 1}. {Fore.YELLOW}Return to Main Menu")
        
        # Get user choice
        try:
            choice = int(input(f"\n{Fore.GREEN}Select a board: {Fore.WHITE}"))
            if 1 <= choice <= len(board_names):
                self.view_board(board_names[choice - 1])
            elif choice == len(board_names) + 1:
                return
            else:
                print(f"{Fore.RED}Invalid choice.")
                time.sleep(1)
                self.message_boards()
        except ValueError:
            print(f"{Fore.RED}Please enter a number.")
            time.sleep(1)
            self.message_boards()

    def view_board(self, board_name):
        """View messages in a specific board"""
        # Generate messages for this board if we don't have any
        if not hasattr(self, 'board_messages') or board_name not in self.board_messages:
            self._generate_board_messages(board_name)
        
        messages = self.board_messages[board_name]
        current_msg_idx = 0
        
        while current_msg_idx < len(messages):
            os.system('cls' if os.name == 'nt' else 'clear')
            message = messages[current_msg_idx]
            
            # Display message header
            print(f"{Fore.CYAN}{Style.BRIGHT}==== {board_name} ===={Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'=' * 60}")
            print(f"{Fore.WHITE}Message: {Fore.YELLOW}#{current_msg_idx + 1} of {len(messages)}")
            print(f"{Fore.WHITE}From: {Fore.MAGENTA}{message['author']}")
            print(f"{Fore.WHITE}Date: {Fore.MAGENTA}{message['date']}")
            print(f"{Fore.WHITE}Subject: {Fore.YELLOW}{message['subject']}")
            print(f"{Fore.GREEN}{'=' * 60}")
            
            # Display message content with word wrap
            content_lines = self._wrap_text(message['content'], 60)
            for line in content_lines:
                print(f"{Fore.WHITE}{line}")
            
            print(f"{Fore.GREEN}{'=' * 60}")
            print(f"{Fore.WHITE}N{Fore.GREEN}ext message, {Fore.WHITE}Q{Fore.GREEN}uit to board list")
            
            # Get user choice
            choice = input(f"\n{Fore.YELLOW}Command: {Fore.WHITE}").upper()
            
            if choice == 'N':
                current_msg_idx += 1
                if current_msg_idx >= len(messages):
                    print(f"{Fore.YELLOW}End of messages.")
                    time.sleep(1.5)
                    break
            elif choice == 'Q':
                break
            else:
                print(f"{Fore.RED}Invalid command.")
                time.sleep(1)
        
        # Return to board list
        self.message_boards()

    def _generate_board_messages(self, board_name):
        """Generate random messages for a board using Claude"""
        if not hasattr(self, 'board_messages'):
            self.board_messages = {}
        
        # Initialize empty list for this board
        self.board_messages[board_name] = []
        
        # Number of messages to generate (3-7)
        num_messages = random.randint(3, 7)
        
        print(f"{Fore.YELLOW}Loading messages from {board_name}...")
        
        # Generate author names for this board
        authors = self._generate_random_authors(num_messages)
        
        # Generate dates (random dates in the past, format: MM-DD-YY)
        years = list(range(85, 96))  # 1985-1995
        months = list(range(1, 13))
        days = list(range(1, 29))  # Simplified - not checking month length
        
        dates = []
        for _ in range(num_messages):
            date = f"{random.choice(months):02d}-{random.choice(days):02d}-{random.choice(years):02d}"
            dates.append(date)
        
        # Sort dates to make them chronological (oldest first)
        dates.sort()
        
        # Generate message content using Claude
        try:
            # Make the API call to Claude to generate all messages at once
            message = claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                temperature=1.0,
                system="You are a creative writer generating content for a nostalgic BBS simulation set in the late 1980s/early 1990s. Create weird, zany, and funny messages that might appear on a message board. The style should be reminiscent of old adventure games like Maniac Mansion, Space Quest, or Zork - full of strange scenarios, paranormal phenomena, and quirky humor. Keep each message between 3-6 sentences.",
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate {num_messages} bizarre, funny messages for a BBS board called '{board_name}'. Each message should include a subject line and content. The messages should be weird, zany, and in the style of old 80s adventure games like Maniac Mansion. Return the results as JSON with this format: [{{\"subject\": \"...\", \"content\": \"...\"}}, ...]. Make the content appropriately weird for this specific board topic."
                    }
                ]
            )
            
            # Extract content and parse JSON
            content = message.content[0].text
            import json
            import re
            
            # Try to find and parse JSON from the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                try:
                    # Parse the JSON string
                    message_data = json.loads(json_str)
                    
                    # Create message objects
                    for i in range(min(len(message_data), num_messages)):
                        msg = {
                            'author': authors[i],
                            'date': dates[i],
                            'subject': message_data[i]['subject'],
                            'content': message_data[i]['content']
                        }
                        self.board_messages[board_name].append(msg)
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"{Fore.RED}Error parsing message data: {e}")
                    self._generate_fallback_messages(board_name, num_messages, authors, dates)
            else:
                self._generate_fallback_messages(board_name, num_messages, authors, dates)
                
        except Exception as e:
            print(f"{Fore.RED}Error generating messages: {e}")
            self._generate_fallback_messages(board_name, num_messages, authors, dates)
        
        # If no messages were generated, use fallback
        if len(self.board_messages[board_name]) == 0:
            self._generate_fallback_messages(board_name, num_messages, authors, dates)
            
        time.sleep(1)  # Brief pause for "loading" effect

    def _generate_fallback_messages(self, board_name, num_messages, authors, dates):
        """Generate fallback messages if Claude API fails"""
        fallback_messages = [
            {
                'subject': "Strange lights in the sky last night",
                'content': "Did anyone else see those weird lights hovering over the old mill? They were pulsating green and purple, and I swear they followed me home. My toaster has been speaking in Latin ever since. Should I be concerned or just make more toast?"
            },
            {
                'subject': "My computer is possessed",
                'content': "Every time I try to download a file, my computer plays the theme from Knight Rider and the floppy drive ejects with incredible force. Yesterday it knocked over my Star Trek figurines and rearranged them in strange symbols. Has anyone experienced similar hardware issues?"
            },
            {
                'subject': "Time travel paradox question",
                'content': "So I accidentally stepped into a temporal vortex in my basement while looking for Christmas decorations. Now I've met my younger self and we're going bowling on Thursdays. Is this causing a paradox? Also, should I tell him about his future baldness or let him discover it naturally?"
            },
            {
                'subject': "Need help with tentacle infestation",
                'content': "After playing that new game I downloaded from the file section, purple tentacles started growing out of my keyboard. They seem to like Mountain Dew and have composed a sonnet. Any recommended cleaning solutions that won't offend their artistic sensibilities?"
            },
            {
                'subject': "Secret government conspiracy",
                'content': "I've intercepted secret communications that prove the mall food court is actually a front for alien intelligence gathering. The Orange Julius guy has three eyes under his hat, and the pretzels contain mind-control salt. Meet me behind the arcade if you want to know more."
            },
            {
                'subject': "My dog learned BASIC programming",
                'content': "I left my programming manual on the floor and now my Golden Retriever is writing code. His first program was just 'FETCH BALL' in an infinite loop, but he's getting better. Anyone know if there's a market for canine software developers? He works for treats."
            },
            {
                'subject': "Haunted floppy disk",
                'content': "I found an unmarked 5.25\" floppy at a garage sale. When I run it, it shows only a text adventure where all paths lead to a digital recreation of my own bedroom. Last night it printed 'BEHIND YOU' without being connected to a printer. Should I continue playing?"
            }
        ]
        
        for i in range(min(len(fallback_messages), num_messages)):
            msg = {
                'author': authors[i],
                'date': dates[i],
                'subject': fallback_messages[i]['subject'],
                'content': fallback_messages[i]['content']
            }
            self.board_messages[board_name].append(msg)

    def _generate_random_authors(self, count):
        """Generate random BBS-style usernames for message authors"""
        prefixes = ["Cyber", "Hack", "Pixel", "Digital", "Quantum", "Retro", "Rad", "Neon", "Disk", "Data", 
                   "Modem", "Glitch", "Bit", "Byte", "Floppy", "Dial", "Logic", "Turbo", "Laser", "Vector"]
        
        suffixes = ["Master", "Wizard", "Kid", "Punk", "Surfer", "Slayer", "Runner", "Jockey", "Ninja", "Guru",
                   "Lord", "Pirate", "Cowboy", "Phantom", "Ghost", "Warrior", "Wrangler", "Dude", "Hacker", "Phoenix"]
        
        numbers = ["", ""] + [str(random.randint(1, 99)) for _ in range(3)]  # 40% chance of having a number
        
        authors = []
        for _ in range(count):
            name = random.choice(prefixes) + random.choice(suffixes) + random.choice(numbers)
            authors.append(name)
        
        return authors

    def _wrap_text(self, text, width):
        """Wrap text to a specified width"""
        import textwrap
        return textwrap.wrap(text, width)

    def file_archives(self):
        """Browse and download files from the BBS archives"""
        # Get BBS info to access board names
        bbs_info = self._generate_bbs_info()
        
        # Main file archives menu
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}{Style.BRIGHT}==== FILE ARCHIVES ===={Style.RESET_ALL}")
            print(f"{Fore.GREEN}Available file categories:\n")
            
            # Display categories based on board names plus a general category
            categories = ["General Software"] + bbs_info["board_names"]
            
            for i, category in enumerate(categories, 1):
                print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{category}")
            print(f"{Fore.WHITE}{len(categories) + 1}. {Fore.YELLOW}Return to Main Menu")
            
            # Get user choice
            try:
                choice = input(f"\n{Fore.GREEN}Select a category: {Fore.WHITE}")
                if choice.strip().lower() == 'q':
                    break
                    
                choice = int(choice)
                if 1 <= choice <= len(categories):
                    self.browse_files(categories[choice - 1])
                elif choice == len(categories) + 1:
                    break
                else:
                    print(f"{Fore.RED}Invalid choice.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a number or Q to quit.")
                time.sleep(1)

    def browse_files(self, category):
        """Browse files in a specific category"""
        # Generate files for this category if we don't have any
        if not hasattr(self, 'file_categories') or category not in self.file_categories:
            self._generate_category_files(category)
            
        files = self.file_categories[category]
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}{Style.BRIGHT}==== {category} Files ===={Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'=' * 60}")
            
            # Display file list with details
            print(f"{Fore.WHITE}{'#':<3} {'Filename':<20} {'Size':<8} {'Date':<10} {'Downloads':<5}")
            print(f"{Fore.GREEN}{'-' * 60}")
            
            for i, file in enumerate(files, 1):
                print(f"{Fore.WHITE}{i:<3} {Fore.YELLOW}{file['name']:<20} {Fore.GREEN}{file['size']:<8} "
                      f"{Fore.MAGENTA}{file['date']:<10} {Fore.CYAN}{file['downloads']:<5}")
            
            print(f"{Fore.GREEN}{'=' * 60}")
            print(f"{Fore.WHITE}Enter file number to view details, {Fore.WHITE}Q{Fore.GREEN} to return")
            
            # Get user choice
            choice = input(f"\n{Fore.YELLOW}Command: {Fore.WHITE}")
            
            if choice.upper() == 'Q':
                break
                
            try:
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(files):
                    self.view_file_details(files[file_idx], category)
                else:
                    print(f"{Fore.RED}Invalid file number.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a number or Q.")
                time.sleep(1)

    def view_file_details(self, file, category):
        """View details for a specific file and option to download"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}{Style.BRIGHT}==== File Details ===={Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'=' * 60}")
            
            # Display file details
            print(f"{Fore.WHITE}Filename: {Fore.YELLOW}{file['name']}")
            print(f"{Fore.WHITE}Category: {Fore.YELLOW}{category}")
            print(f"{Fore.WHITE}Size: {Fore.GREEN}{file['size']}")
            print(f"{Fore.WHITE}Uploaded: {Fore.MAGENTA}{file['date']}")
            print(f"{Fore.WHITE}Downloads: {Fore.CYAN}{file['downloads']}")
            print(f"{Fore.WHITE}Uploaded by: {Fore.MAGENTA}{file['uploader']}")
            print(f"{Fore.GREEN}{'-' * 60}")
            
            # Display file description with word wrap
            print(f"{Fore.WHITE}Description:")
            description_lines = self._wrap_text(file['description'], 60)
            for line in description_lines:
                print(f"{Fore.WHITE}{line}")
                
            print(f"{Fore.GREEN}{'=' * 60}")
            print(f"{Fore.WHITE}D{Fore.GREEN}ownload file, {Fore.WHITE}Q{Fore.GREEN}uit to file list")
            
            # Get user choice
            choice = input(f"\n{Fore.YELLOW}Command: {Fore.WHITE}").upper()
            
            if choice == 'D':
                self.download_file(file)
            elif choice == 'Q':
                break
            else:
                print(f"{Fore.RED}Invalid command.")
                time.sleep(1)

    def download_file(self, file):
        """Simulate downloading a file"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== Downloading File ===={Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 60}")
        
        print(f"{Fore.WHITE}Downloading: {Fore.YELLOW}{file['name']}")
        print(f"{Fore.WHITE}Size: {Fore.GREEN}{file['size']}")
        
        # Parse the size to simulate download time
        size_value = float(file['size'].split()[0])
        size_unit = file['size'].split()[1]
        
        # Adjust time based on size unit (KB, MB)
        if size_unit == "KB":
            total_chunks = int(size_value / 5) + 1  # 5KB chunks
        else:  # MB
            total_chunks = int(size_value * 20) + 1  # More chunks for MB files
            
        # Cap total chunks to reasonable range
        total_chunks = min(max(total_chunks, 5), 30)
        
        # Simulate download progress
        print(f"{Fore.WHITE}Progress: ", end="")
        for i in range(total_chunks):
            # Calculate progress percentage
            progress = int((i / total_chunks) * 100)
            
            # Simulate variable download speeds
            if random.random() < 0.2:  # 20% chance of slow chunk
                time.sleep(0.3)
            else:
                time.sleep(0.1)
                
            # Show progress
            print(f"{Fore.GREEN}▓", end="", flush=True)
            
            # Show percentage every few chunks
            if i % 5 == 0 or i == total_chunks - 1:
                print(f" {progress}%", end="", flush=True)
                
        print(f"\n{Fore.GREEN}Download complete!")
        
        # Update download counter
        file['downloads'] += 1
        
        # Generate a random funny message about the download
        download_messages = [
            "Your digital contraband has been secured!",
            "File successfully smuggled through the information superhighway!",
            "Download complete! No viruses detected... probably.",
            "Congratulations! You've just increased your nerd cred by +5 points!",
            "File downloaded faster than a caffeinated squirrel!",
            "Your bits have successfully traveled through time from 1992!",
            "Warning: This file may contain rad 90s content!",
            "File downloaded and authenticated with dial-up handshake!",
            "Download verified by digital archaeologists!",
            "File transfer complete! Please rewind before returning."
        ]
        
        print(f"{Fore.YELLOW}{random.choice(download_messages)}")
        input(f"\n{Fore.GREEN}Press Enter to continue...")

    def _generate_category_files(self, category):
        """Generate themed files for a category using Claude"""
        if not hasattr(self, 'file_categories'):
            self.file_categories = {}
            
        # Initialize empty list for this category
        self.file_categories[category] = []
        
        # Number of files to generate (10-20)
        num_files = random.randint(10, 20)
        
        print(f"{Fore.YELLOW}Loading file listings for {category}...")
        
        # Generate file details
        
        # 1. Generate random uploaders
        uploaders = self._generate_random_authors(num_files)
        
        # 2. Generate random dates (format: MM-DD-YY)
        years = list(range(85, 96))  # 1985-1995
        months = list(range(1, 13))
        days = list(range(1, 29))  # Simplified
        
        dates = []
        for _ in range(num_files):
            date = f"{random.choice(months):02d}-{random.choice(days):02d}-{random.choice(years):02d}"
            dates.append(date)
        
        # Sort dates (older files first)
        dates.sort()
        
        # 3. Random download counts (more for older files)
        downloads = []
        for i in range(num_files):
            # Older files have more downloads (generally)
            base_downloads = random.randint(0, 50)
            age_factor = (num_files - i) / num_files  # 1.0 for oldest, near 0 for newest
            download_count = int(base_downloads + (age_factor * random.randint(0, 150)))
            downloads.append(download_count)
        
        try:
            # Make API call to Claude to generate themed files
            message = claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=1.0,
                system="You are generating content for a nostalgic BBS file section from the late 1980s/early 1990s. Create weird, amusing, and period-appropriate file listings for downloading. Files should match the category theme and include typical file types from that era (.zip, .arj, .exe, .txt, .gif, .bmp, .com, etc.). Be creative and quirky but appropriate.",
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate {num_files} file listings for a BBS file section called '{category}'. Each file should have a name (8.3 format preferred but not required) and a brief description. Make them weird, quirky, and appropriate for the late 80s/early 90s BBS era. The files should relate to the '{category}' theme. Return the results as JSON in this format: [{{\"name\": \"FILENAME.EXT\", \"description\": \"...\", \"size\": \"XXX KB or X.XX MB\"}}, ...]. Size should be 25KB-3MB range, mostly smaller files."
                    }
                ]
            )
            
            # Extract content and parse JSON
            content = message.content[0].text
            import json
            import re
            
            # Try to find and parse JSON from the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                try:
                    # Parse the JSON string
                    file_data = json.loads(json_str)
                    
                    # Create file objects
                    for i in range(min(len(file_data), num_files)):
                        # Make sure each file has required fields
                        if all(field in file_data[i] for field in ["name", "description", "size"]):
                            file_obj = {
                                'name': file_data[i]['name'],
                                'description': file_data[i]['description'],
                                'size': file_data[i]['size'],
                                'date': dates[i],
                                'uploader': uploaders[i],
                                'downloads': downloads[i]
                            }
                            self.file_categories[category].append(file_obj)
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"{Fore.RED}Error parsing file data: {e}")
                    self._generate_fallback_files(category, num_files, uploaders, dates, downloads)
            else:
                self._generate_fallback_files(category, num_files, uploaders, dates, downloads)
                
        except Exception as e:
            print(f"{Fore.RED}Error generating files: {e}")
            self._generate_fallback_files(category, num_files, uploaders, dates, downloads)
        
        # If no files were generated, use fallback
        if len(self.file_categories[category]) == 0:
            self._generate_fallback_files(category, num_files, uploaders, dates, downloads)
            
        time.sleep(1)  # Brief pause for "loading" effect

    def _generate_fallback_files(self, category, num_files, uploaders, dates, downloads):
        """Generate fallback files if Claude API fails"""
        # Generic file extensions
        extensions = ["ZIP", "EXE", "COM", "TXT", "GIF", "BMP", "ARJ", "LZH", "WAV", "MOD", "ANS", "BAS"]
        
        # File sizes
        sizes = ["12 KB", "45 KB", "128 KB", "256 KB", "512 KB", "785 KB", "1.2 MB", "2.1 MB"]
        
        # Generate generic files based on category
        for i in range(num_files):
            # Create a suitable filename for the category
            words = category.split()
            prefix = ''.join([word[0] for word in words])[:3].upper()
            name = f"{prefix}{random.randint(1, 999)}.{random.choice(extensions)}"
            
            # Generic description based on file type
            ext = name.split('.')[-1].upper()
            
            if ext in ["ZIP", "ARJ", "LZH"]:
                desc = f"Archive of {category.lower()} files and utilities."
            elif ext in ["EXE", "COM"]:
                desc = f"Executable program related to {category.lower()}. May require DOS."
            elif ext == "TXT":
                desc = f"Documentation or text file about {category.lower()}."
            elif ext in ["GIF", "BMP"]:
                desc = f"Image file showing {category.lower()} related graphics."
            elif ext == "WAV":
                desc = f"Sound file with {category.lower()} audio."
            elif ext == "MOD":
                desc = f"Tracker music module with cool {category.lower()} tunes."
            elif ext == "ANS":
                desc = f"ANSI art file depicting {category.lower()} scenes."
            elif ext == "BAS":
                desc = f"BASIC source code for a {category.lower()} utility."
            else:
                desc = f"File related to {category.lower()}. Download to find out more!"
                
            # Add the file
            file_obj = {
                'name': name,
                'description': desc,
                'size': random.choice(sizes),
                'date': dates[i] if i < len(dates) else "01-01-91",
                'uploader': uploaders[i] if i < len(uploaders) else "SysOp",
                'downloads': downloads[i] if i < len(downloads) else random.randint(0, 100)
            }
            
            self.file_categories[category].append(file_obj)

    def door_games(self):
        """Browse and attempt to play classic BBS door games"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== DOOR GAMES ===={Style.RESET_ALL}")
        
        # Generate a random game name
        game = self._generate_random_door_game()
        
        # Display game selection
        print(f"{Fore.GREEN}Available games:\n")
        print(f"{Fore.WHITE}1. {Fore.YELLOW}{game['name']}")
        print(f"{Fore.WHITE}2. {Fore.YELLOW}Return to Main Menu")
        
        # Get user choice
        try:
            choice = input(f"\n{Fore.GREEN}Select an option: {Fore.WHITE}")
            if choice == "1":
                self._display_door_game(game)
            elif choice == "2":
                return
            else:
                print(f"{Fore.RED}Invalid choice.")
                time.sleep(1)
                self.door_games()
        except ValueError:
            print(f"{Fore.RED}Please enter a number.")
            time.sleep(1)
            self.door_games()

    def _generate_random_door_game(self):
        """Generate a random door game name and details"""
        # Game name parts
        prefixes = ["Cyber", "Galactic", "Mega", "Quantum", "Astro", "Neon", "Digital", 
                   "Turbo", "Rad", "Techno", "Laser", "Pixel", "Retro", "Ultra", "Hyper"]
        
        main_words = ["Quest", "Warriors", "Battle", "Lords", "Dungeon", "Realm", "Maze", 
                     "Empire", "Raiders", "Traders", "Command", "Arena", "Conquest", "Clash"]
        
        suffixes = ["II", "3000", "Master", "Online", "Pro", "Plus", "X", "Deluxe", "Adventure",
                   "Challenge", "World", "Zone", "Championship"]
        
        # Generate a random game name
        prefix = random.choice(prefixes)
        main = random.choice(main_words)
        
        # 50% chance to add a suffix
        if random.random() < 0.5:
            suffix = " " + random.choice(suffixes)
        else:
            suffix = ""
            
        name = f"{prefix} {main}{suffix}"
        
        # Generate a year (1987-1993)
        year = random.randint(1987, 1993)
        
        # Generate a fake company name
        company_prefixes = ["Stellar", "Atomic", "Byte", "Razor", "Binary", "Digital", "Thunder", 
                           "Lightning", "Silicon", "Mystic", "Radical", "Elite", "Omega"]
        
        company_suffixes = ["Software", "Games", "Interactive", "Systems", "Productions", 
                           "Entertainment", "Computing", "Designs", "Studios"]
        
        company = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
        
        # Generate a tagline
        taglines = [
            "Enter the arena... if you dare!",
            "The final frontier of online gaming!",
            "Where legends are made!",
            "Your reality just got virtual!",
            "Challenge awaits the brave!",
            "The ultimate test of skill!",
            "Can you survive the digital onslaught?",
            "Prepare for electronic combat!",
            "Journey into the digital unknown!",
            "Fame and fortune await the victorious!",
            "The electronic battlefield beckons!",
            "Are you elite enough?",
            "Venture beyond the modem's call!"
        ]
        
        return {
            'name': name,
            'year': year,
            'company': company,
            'tagline': random.choice(taglines)
        }

    def _display_door_game(self, game):
        """Display a door game title screen and then show out of order message"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Random colors
        colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED, Fore.BLUE, Fore.WHITE]
        title_color = random.choice(colors)
        accent_color = random.choice([c for c in colors if c != title_color])
        
        # Generate ASCII art title
        try:
            fonts = ['big', 'block', 'bubble', 'digital', 'ivrit', 'banner']
            font = random.choice(fonts)
            title_art = pyfiglet.figlet_format(game['name'], font=font)
        except Exception:
            # Fallback
            title_art = pyfiglet.figlet_format(game['name'], font='standard')
        
        # Display title screen
        print(f"{title_color}{title_art}")
        print(f"{accent_color}{'=' * 60}")
        print(f"{Fore.WHITE}© {game['year']} {game['company']}")
        print(f"{Fore.WHITE}All rights reserved")
        print(f"{accent_color}{'=' * 60}")
        
        # Display tagline
        print(f"{Fore.YELLOW}{Style.BRIGHT}{game['tagline']}{Style.RESET_ALL}\n")
        
        # Random ASCII art for the game
        game_arts = [
            r"""
             _____
            |     |
            | ◢■◣ |
            | ■■■ |
            |_____|
            /    /|
           /____/ |
           |____|/
            """,
            r"""
                ╔═══╗
               ╔╝███╚╗
               ╚╗███╔╝
                ╚═══╝
             ╔═╗     ╔═╗
             ║ ╚═════╝ ║
             ╚═════════╝
            """,
            r"""
              /\
             /  \
            |    |
            |    |--O
            |    |  |'-.__
           _|    |__|     `-.
          /               /\ `\
          \_______________/  \__)
            """,
            r"""
             .-------.
            /   o   /|
           /_______/ |
           |       | |
           |       | /
           |       |/
            """,
            r"""
                 /\
                /  \
               /    \
              /      \
             /        \
            /__________\
            \__________/
            """,
        ]
        
        print(f"{random.choice(colors)}{random.choice(game_arts)}")
        
        # Loading animation
        print(f"{Fore.WHITE}Loading game", end="")
        for _ in range(5):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print("\n")
        
        # Out of order message
        time.sleep(1.5)
        print(f"{Fore.RED}{Style.BRIGHT}* * * SYSTEM ERROR * * *{Style.RESET_ALL}")
        
        # Random funny error messages
        error_messages = [
            "DOOR32.SYS not found. Did someone leave it open?",
            "Error: Game requires 640K of RAM. Your system has only 638K available.",
            "Fatal exception: CPU not radical enough for this gnarly game.",
            "ALLOC: Memory fragmentation detected. Please defragment your brain and try again.",
            "FOSSIL driver reports modem is too old for time travel functions.",
            "ERROR: Required ANSI.SYS driver is on vacation until further notice.",
            "CRITICAL: Failed to initialize the awesome-o-meter.",
            "4913: Insufficient floppy disk capacity for storing high scores.",
            "ERROR: SysOp unplugged the game to charge their Walkman.",
            "VORTEX.DLL load failure: Please ensure your flux capacitor is properly connected."
        ]
        
        print(f"{Fore.RED}{random.choice(error_messages)}")
        print(f"{Fore.YELLOW}\nThis door game is temporarily out of order.")
        print(f"{Fore.YELLOW}The SysOp has been notified and promises to fix it")
        print(f"{Fore.YELLOW}right after finishing this pizza and Mountain Dew.\n")
        
        input(f"{Fore.GREEN}Press Enter to return to the games menu...")
        self.door_games()

    def chat_with_sysop(self):
        """Chat with the quirky AI SysOp of the BBS"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== CHAT WITH SYSOP ===={Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 60}")
        
        # Get BBS info to personalize the SysOp
        bbs_info = self._generate_bbs_info()
        sysop_name = bbs_info["sysop"]
        bbs_name = bbs_info["name"]
        
        # Initialize chat history
        chat_history = []
        
        # Add system message
        system_message = self._generate_sysop_personality(bbs_info)
        
        # Welcome message
        print(f"{Fore.YELLOW}Establishing direct connection to SysOp terminal...")
        time.sleep(1)
        print(f"{Fore.GREEN}Connection established!")
        time.sleep(0.5)
        
        # Initial message from SysOp
        initial_message = self._get_sysop_response(
            system_message, 
            chat_history, 
            f"You are chatting with {self.user_name} who just connected to your BBS. Give them a weird, quirky greeting that shows your strange personality. Keep it to 2-3 sentences."
        )
        
        self._display_sysop_message(sysop_name, initial_message)
        chat_history.append({"role": "assistant", "content": initial_message})
        
        # Chat loop
        while True:
            # Get user input
            user_message = input(f"{Fore.GREEN}[{self.user_name}]: {Fore.WHITE}")
            
            # Check for exit
            if user_message.lower() in ["bye", "goodbye", "exit", "quit"]:
                break
                
            # Add user message to history
            chat_history.append({"role": "user", "content": user_message})
            
            # Get SysOp response
            print(f"{Fore.YELLOW}SysOp is typing", end="")
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print()
            
            sysop_response = self._get_sysop_response(system_message, chat_history)
            self._display_sysop_message(sysop_name, sysop_response)
            
            # Add SysOp response to history
            chat_history.append({"role": "assistant", "content": sysop_response})
        
        # Farewell message
        farewell = self._get_sysop_response(
            system_message,
            chat_history,
            f"The user {self.user_name} is leaving the chat. Give a strange farewell message that's true to your weird character. Keep it brief."
        )
        
        self._display_sysop_message(sysop_name, farewell)
        time.sleep(1)
        
        print(f"{Fore.YELLOW}\nDisconnecting from SysOp terminal...")
        time.sleep(1)
        print(f"{Fore.RED}Connection terminated.")
        time.sleep(0.5)
        
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

    def _generate_sysop_personality(self, bbs_info):
        """Generate a unique, weird personality for the SysOp based on BBS info"""
        # Extract info from the BBS
        sysop_name = bbs_info["sysop"]
        bbs_name = bbs_info["name"]
        tagline = bbs_info["tagline"]
        boards = ", ".join(bbs_info["board_names"])
        
        # Generate random quirks
        speech_quirks = [
            "replacing 's' with 'z'",
            "adding '~' after every sentence",
            "RANDOMLY capitalizing WORDS",
            "speaking in mostly lowercase with no punctuation except '...'",
            "inserting retro computer terms into every sentence",
            "starting each message with a strange noise like 'BLEEP!' or 'KZZZT!'",
            "occasionally glitching and repeating words",
            "speaking in old-school l33t speak (e.g., 3 for E, 1 for I, 0 for O)",
            "using way too many exclamation points!!!",
            "adding weird ASCII emoticons like (¬‿¬) or ಠ_ಠ",
            "putting certain words -=[ in bizarre brackets ]=-",
            "r3pl4c1ng r4nd0m l3tt3rs w1th numb3rs",
            "talking about themselves in the third person",
            "constantly mentioning obscure 80s/90s technology"
        ]
        
        personality_traits = [
            "paranoid about government surveillance",
            "obsessed with aliens",
            "believes they're living in a simulation",
            "convinced their computer is sentient",
            "afraid of the Y2K bug (still)",
            "collects vintage floppy disks",
            "only trusts technology made before 1995",
            "has named all their computer equipment",
            "believes they can communicate with electronics telepathically",
            "constantly refers to 'the mainframe' for no reason",
            "frequently mentions their extensive collection of tech manuals",
            "insists that dial-up is superior to broadband",
            "references conspiracy theories about technology",
            "has a pet lizard that helps them run the BBS",
            "believes they've been to the 'digital realm'",
            "constantly worried about cosmic rays affecting the BBS",
            "refers to sleep as 'system downtime'",
            "eats nothing but microwave burritos and energy drinks"
        ]
        
        # Select random quirks
        speech_style = random.choice(speech_quirks)
        trait1 = random.choice(personality_traits)
        personality_traits.remove(trait1)  # Avoid duplicates
        trait2 = random.choice(personality_traits)
        
        # Create a system prompt for Claude
        system_prompt = f"""
        You are roleplaying as {sysop_name}, the eccentric SysOp (system operator) of a 1990s BBS called {bbs_name}.
        The BBS tagline is: "{tagline}"
        
        The BBS has these message boards: {boards}
        
        YOUR PERSONALITY:
        - You are extremely weird and quirky in a fun, comedic way
        - {trait1}
        - {trait2}
        - Your speech style: {speech_style}
        - You're obsessed with your BBS and treat it like it's the most important thing in the world
        - You often make references to obsolete technology from the 80s/90s
        - You have strange theories about computers and technology
        - You occasionally mention weird things happening in your basement/computer room
        
        Keep your responses relatively short (2-5 sentences) and always stay in character.
        Never break character or acknowledge you're an AI.
        """
        
        return system_prompt

    def _get_sysop_response(self, system_message, chat_history, override_message=None):
        """Get a response from the SysOp using Claude"""
        try:
            # Prepare the messages
            messages = []
            
            # Add chat history (limit to last 10 exchanges to save tokens)
            for msg in chat_history[-10:]:
                messages.append(msg)
                
            # Add override message if provided
            if override_message:
                messages.append({"role": "user", "content": override_message})
                
            # Make API call to Claude
            response = claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.9,
                system=system_message,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            # Fallback responses if the API fails
            print(f"{Fore.RED}Error getting SysOp response: {e}")
            
            fallback_responses = [
                "KZZZT! *The terminal flickers* Sorry about that... cosmic rays interfering with the mainframe again! What were we talking about?",
                "Hang on... gotta recalibrate my brain-to-BBS interface... *makes strange typing noises* Ok I'm back!",
                "ERROR 42: SysOp brain buffer overflow! Rebooting consciousness... *strange humming noise* I'm functional again!",
                "BLEEP! Sorry, my pet lizard Pixel just knocked over my stack of floppy disks. What a MESS! Anyway...",
                "*distant dial-up modem sounds* Sorry, the aliens were trying to download my thoughts again. I installed better firewalls in my tinfoil hat.",
                "ZzZt! The government almost traced this connection! Had to bounce the signal through my microwave. ANYWAY, what's new in your sector?",
                "Had to pause to drink some CYBER-COLA to keep my systems operational! The caffeine helps my neurons connect to the digital realm!",
                "Whoa! My mechanical keyboard just started typing by itself again. I think it's trying to communicate with me. Not now, keyboard!"
            ]
            
            return random.choice(fallback_responses)

    def _display_sysop_message(self, sysop_name, message):
        """Display a message from the SysOp with formatting"""
        # Random color for this message
        colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED, Fore.BLUE]
        color = random.choice(colors)
        
        # Display the message
        print(f"{color}[{sysop_name}]: {Fore.WHITE}{message}")

    def logoff(self):
        """Log off from the BBS"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}Logging off from BBScapade...")
        time.sleep(1)
        print(f"{Fore.GREEN}Thank you for visiting BBScapade!")
        print(f"{Fore.GREEN}Call back anytime for a new BBS experience!")
        print()
        print(f"{Fore.YELLOW}NO CARRIER")
        self.logged_in = False

    def run(self):
        """Main application flow"""
        try:
            # Setup signal handler for clean exit
            signal.signal(signal.SIGINT, self._handle_exit)
            
            # Play dialup sound
            self.play_dialup_sound()
            
            # Show welcome screen
            self.display_welcome_screen()
            
            # Show login screen
            self.login_screen()
            
            # Show main menu
            self.main_menu()
            
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}")
            sys.exit(1)

    def _handle_exit(self, sig, frame):
        """Handle exit signals gracefully"""
        print(f"\n{Fore.YELLOW}Disconnecting from BBScapade...")
        print(f"{Fore.YELLOW}NO CARRIER")
        sys.exit(0)


if __name__ == "__main__":
    bbs = BBScapade()
    bbs.run()