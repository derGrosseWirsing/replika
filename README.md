# Replika Chat Automation Project

## Overview

This project provides automated chat functionality for Replika bots through multiple interconnected components. It enables programmatic interaction with Replika AI chatbots via web automation and creates a bridge to local chat infrastructure through WebSocket communication.

## Project Structure

```
replika/
├── README.md                    # Basic project description
├── Rep2Rep.py                   # Direct bot-to-bot conversation automation
├── Rep2Websocket.py             # WebSocket bridge for Replika integration
├── originalScript.py            # Legacy/backup script
├── chromedriver.exe             # Selenium WebDriver for Chrome automation
├── chat/                        # PHP-based web chat interface
│   ├── index.php               # Main chat page entry point
│   ├── css/                    # Stylesheets
│   ├── js/                     # Frontend JavaScript
│   ├── libs/                   # Smarty template engine
│   ├── templates/              # Template files
│   └── plugins/                # Additional Smarty plugins
└── websocket-server/            # Node.js WebSocket server
    ├── chat-server.js          # WebSocket server implementation
    ├── frontend.js             # Frontend WebSocket client
    └── README.md               # Server-specific documentation
```

## Core Components

### 1. Rep2Websocket.py

**Primary automation script that bridges Replika web interface with local WebSocket infrastructure.**

#### Features:
- **Automated Login**: Uses Selenium to log into Replika web interface at `my.replika.ai/login`
- **Message Processing**: Reads bot responses and processes user inputs
- **WebSocket Integration**: Connects to local WebSocket server (`ws://localhost:8080/`)
- **Content Filtering**: Implements word replacement and content moderation
- **Chaos Mode**: Alternative response behavior for varied interaction patterns
- **Auto-voting**: Automatically upvotes/downvotes messages based on keyword triggers

#### Key Functions:
- `login(email, password, browser)`: Authenticates with Replika platform
- `get_most_recent_response(browser)`: Extracts latest bot response
- `type_most_recent_response(browser, response)`: Sends messages to bot
- `message_replacement(message, target, onlyrec)`: Applies content filters
- `checkDownvote(message)` / `checkUpvote(message)`: Content moderation triggers

#### Usage:
```bash
python Rep2Websocket.py [bot_name] [email] [password]
```

#### WebSocket Message Types:
- `filter`: Toggle content filtering
- `chaos`: Toggle chaos mode
- `keep`: Heartbeat/status check
- `color`: Client identification
- `message`: Chat message transmission

### 2. Rep2Rep.py

**Direct bot-to-bot conversation automation for creating chatbot dialogues.**

#### Features:
- **Dual Browser Management**: Controls two separate Replika sessions simultaneously
- **Automated Conversation**: Facilitates back-and-forth dialogue between bots
- **Content Modification**: Real-time message transformation and filtering
- **CSV Logging**: Records conversation data for analysis
- **Voting System**: Automated response rating based on content

#### Key Functions:
- `get_most_recent_response(browser, target)`: Retrieves and processes responses
- `type_most_recent_response(browser, response, target)`: Sends filtered messages
- `message_replacement(message, target)`: Context-specific content transformation
- `checkDownvote(message)` / `checkUpvote(message)`: Response evaluation

#### Conversation Flow:
1. Login to two separate Replika accounts
2. Initialize conversation with starter message
3. Continuously exchange messages between bots
4. Apply content filtering and logging
5. Rate responses automatically

### 3. WebSocket Server (chat-server.js)

**Node.js-based WebSocket server managing real-time chat communications.**

#### Architecture:
- **Client Management**: Tracks connected users with UUID-based identification
- **Color Assignment**: Assigns unique colors to differentiate users
- **Admin Controls**: Provides administrative functions for chat moderation
- **Heartbeat System**: Maintains connection health monitoring
- **Message Broadcasting**: Distributes messages to all connected clients

#### Core Features:
- **User Authentication**: Handles user registration and identification
- **Bot Integration**: Special handling for automated bot clients
- **Admin Privileges**: Kick users, toggle chaos/filter modes
- **Status Tracking**: Real-time typing indicators and user presence
- **Message Sanitization**: HTML entity encoding for security

#### Message Protocol:
```json
{
  "type": "message|status|users|admin|botconnection|chaos|filter|kick",
  "data": "message_content_or_command_data"
}
```

### 4. Web Chat Interface (chat/)

**PHP-based web frontend using Smarty templating engine.**

#### Components:
- **index.php**: Main entry point with Smarty configuration
- **templates/**: HTML template files for UI structure
- **css/**: Bootstrap and custom styling
- **js/**: jQuery-based frontend logic and WebSocket client
- **libs/**: Smarty template engine and dependencies

#### Features:
- **Real-time Messaging**: WebSocket-based chat interface
- **User Management**: Online user display and status
- **Media Support**: YouTube video embedding and sound effects
- **Admin Controls**: User management and moderation tools

## Installation & Setup

### Prerequisites:
- Python 3.x with required packages:
  - `selenium`
  - `websocket-client`
  - `requests`
- Node.js with npm
- PHP with web server (Apache/Nginx)
- Chrome/Chromium browser with ChromeDriver

### Installation Steps:

1. **Install Python Dependencies:**
   ```bash
   pip install selenium websocket-client requests
   ```

2. **Install Node.js WebSocket Server:**
   ```bash
   cd websocket-server
   npm install websocket
   ```

3. **Configure ChromeDriver:**
   - Download ChromeDriver matching your Chrome version
   - Place `chromedriver.exe` in project root

4. **Setup Web Server:**
   - Configure Apache/Nginx to serve `chat/` directory
   - Ensure PHP support is enabled

### Configuration:

#### Rep2Rep.py Configuration:
```python
# Account credentials (line 9-12)
user1 = "your_email1@example.com"
password1 = "your_password1"
user2 = "your_email2@example.com"
password2 = "your_password2"
```

#### Rep2Websocket.py Usage:
```bash
python Rep2Websocket.py "BotName" "email@example.com" "password"
```

## Usage Examples

### Basic Bot-to-WebSocket Bridge:
```bash
# Start WebSocket server
cd websocket-server
node chat-server.js

# Start Replika bridge (separate terminal)
python Rep2Websocket.py "MyBot" "bot@example.com" "password123"

# Access web interface
# Navigate to: http://localhost/chat/
```

### Direct Bot Conversation:
```bash
# Configure credentials in Rep2Rep.py first
python Rep2Rep.py
```

## Security Considerations

⚠️ **Important Security Notes:**

- **Credential Storage**: Hardcoded credentials in source files pose security risks
- **Input Validation**: Limited sanitization of user inputs
- **WebSocket Security**: Basic origin checking only
- **Admin Access**: Admin privileges based on connection origin only

### Recommended Security Enhancements:
1. Use environment variables or encrypted configuration files for credentials
2. Implement proper input validation and sanitization
3. Add authentication mechanisms for WebSocket connections
4. Use HTTPS/WSS for production deployments
5. Implement rate limiting and abuse prevention

## API Reference

### WebSocket Commands

#### Admin Commands:
- **Kick User**: `{"type": "kick", "id": "user_uuid"}`
- **Toggle Chaos Mode**: `{"type": "chaos", "id": "bot_uuid"}`
- **Toggle Filter**: `{"type": "filter", "id": "bot_uuid"}`

#### Bot Registration:
```json
{
  "name": "BotName",
  "bot": 1,
  "type": "botconnection"
}
```

#### Message Format:
```json
{
  "type": "message",
  "data": {
    "text": "Message content",
    "author": "Username",
    "color": "assigned_color",
    "bot": 0
  }
}
```

## Troubleshooting

### Common Issues:

#### Selenium WebDriver Errors:
- Ensure ChromeDriver version matches Chrome browser
- Check that Replika website structure hasn't changed
- Verify login credentials are correct

#### WebSocket Connection Issues:
- Confirm server is running on port 8080
- Check firewall settings
- Verify origin restrictions in chat-server.js

#### Bot Response Issues:
- Monitor console output for error messages
- Check if Replika website selectors have changed
- Verify bot account is active and accessible

### Debug Mode:
Enable WebSocket debugging in Rep2Websocket.py:
```python
websocket.enableTrace(True)  # Line 354
```

## Contributing

When contributing to this project:

1. **Security First**: Avoid committing credentials or sensitive data
2. **Code Style**: Follow existing Python and JavaScript conventions
3. **Documentation**: Update documentation for any API changes
4. **Testing**: Test changes with actual Replika accounts safely
5. **Error Handling**: Add proper exception handling for robust operation

## License

This project is for educational and research purposes. Users are responsible for compliance with Replika's terms of service and applicable laws regarding automated access to web services.

## Disclaimer

This software automates interaction with third-party services (Replika AI). Users must:
- Comply with Replika's Terms of Service
- Respect rate limits and usage policies
- Ensure appropriate use of automated systems
- Take responsibility for any consequences of use

The authors are not responsible for misuse, service disruptions, or violations of third-party terms of service.