# BBScapade

BBScapade is a nostalgic, AI-powered BBS (Bulletin Board System) simulator that generates unique and hilarious content each time you connect. Written in Python and powered by Claude AI, this application recreates the quirky charm of early 90s BBSes with a modern twist.

> **Note:** This project was created for the Cloudflare AI Hack Night on March 10th, 2025.

## Features

- 🎨 Colorful ANSI text interface
- 🔊 Authentic dialup connection sound
- 🖼️ ASCII art using Figlet
- 🤖 AI-generated content (BBS name, sysop, boards, etc.)
- 📋 Classic BBS menu structure
- 🎮 Simulated message boards, file archives, and door games

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bbscapade.git
   cd bbscapade
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install requirements:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Claude API key:
   ```
   CLAUDE_API_KEY=your_api_key_here
   ```

5. Create an assets folder and add a dialup sound:
   ```
   mkdir assets
   # Add dialup.wav to the assets folder
   ```

## Usage

Run the application:
```
python bbscapade.py
```

## Customization

- Modify the prompts in `_generate_bbs_info()` to change the style of AI-generated content
- Add or remove menu options in the `main_menu()` method
- Implement additional features by completing the placeholder methods

## Requirements

- Python 3.8+
- Claude API key
- External dependencies listed in requirements.txt

## Future Enhancements

- Implement actual message board functionality
- Add simple text-based games
- Create a file sharing simulation
- Add more nostalgic details like ANSI art, slow typing effects, etc.
- Multi-user capabilities

## License

MIT

---

Enjoy your trip down memory lane with a bizarre AI twist! 📟