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
            
            print(f"{Fore.CYAN}{Style.BRIGHT}==== MAIN MENU ===={Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. {Fore.GREEN}Message Boards")
            print(f"{Fore.WHITE}2. {Fore.GREEN}File Archives")
            print(f"{Fore.WHITE}3. {Fore.GREEN}Door Games")
            print(f"{Fore.WHITE}4. {Fore.GREEN}Chat with SysOp (AI)")
            print(f"{Fore.WHITE}5. {Fore.GREEN}User Settings")
            print(f"{Fore.WHITE}6. {Fore.GREEN}About BBScapade")
            print(f"{Fore.WHITE}7. {Fore.GREEN}Logoff")
            
            choice = input(f"\n{Fore.YELLOW}Choose an option: {Fore.WHITE}")
            
            if choice == "1":
                self.message_boards()
            elif choice == "2":
                self.file_archives()
            elif choice == "3":
                self.door_games()
            elif choice == "4":
                self.chat_with_sysop()
            elif choice == "5":
                self.user_settings()
            elif choice == "6":
                self.about()
            elif choice == "7":
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
        """File archives functionality - placeholder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== FILE ARCHIVES ===={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(This feature is not implemented in the skeleton.)")
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

    def door_games(self):
        """Door games functionality - placeholder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== DOOR GAMES ===={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(This feature is not implemented in the skeleton.)")
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

    def chat_with_sysop(self):
        """Chat with AI SysOp functionality - placeholder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== CHAT WITH SYSOP ===={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(This feature is not implemented in the skeleton.)")
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

    def user_settings(self):
        """User settings functionality - placeholder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== USER SETTINGS ===={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(This feature is not implemented in the skeleton.)")
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

    def about(self):
        """About screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== ABOUT BBSCAPADE ===={Style.RESET_ALL}")
        print(f"{Fore.GREEN}BBScapade - A nostalgic BBS experience powered by Claude AI")
        print(f"{Fore.GREEN}Each time you connect, a new, randomly generated BBS is created")
        print(f"{Fore.GREEN}with unique content, message boards, and SysOp personality.")
        print()
        print(f"{Fore.YELLOW}This is a fun project that simulates the BBS experience of")
        print(f"{Fore.YELLOW}the late 80s and early 90s with a modern AI twist.")
        input(f"\n{Fore.GREEN}Press Enter to return to main menu...")

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