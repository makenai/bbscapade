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
        """Message board functionality - placeholder"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}==== MESSAGE BOARDS ===={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(This feature is not implemented in the skeleton.)")
        input(f"{Fore.GREEN}Press Enter to return to main menu...")

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
            # self.play_dialup_sound()
            
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