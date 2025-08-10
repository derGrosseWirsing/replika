## Rep2Websocket:

### Key Features

1.  **Automated Login with Selenium**
    * The script uses [Selenium](https://www.selenium.dev/) to automatically log into the Replika web interface at [my.replika.ai/login](https://my.replika.ai/login) using an email and password.

2.  **Automated Chat Interaction**
    * It automatically reads the chatbot's responses from the web page.
    * It can send messages to the chatbot by typing text into the input field and submitting it.

3.  **WebSocket Server Connection**
    * The script opens a connection to a local WebSocket server (`ws://localhost:8080/`).
    * It can receive and send messages through this interface.

4.  **Filters and "Chaos Mode"**
    * The script can filter incoming and outgoing messages and replace specific words—for example, swapping harmless or inappropriate terms with other words.
    * A "chaos mode" influences how and when the bot responds to messages.

5.  **Automatic Upvote/Downvote**
    * Based on certain keywords, the script can automatically upvote or downvote messages in the chat, for example, in response to inappropriate content.

6.  **Status Transmission**
    * The script reports via WebSocket when the bot is "typing" or has finished responding.

---

### Workflow (Summary)

* **Start**: The script logs into Replika using the provided email, password, and bot name.
* **WebSocket Connection**: It establishes a WebSocket connection to the local server.
* **Receive Commands**: It receives control commands (`filter`, `chaos`) and messages via WebSocket.
* **Message Processing**: Messages are processed as needed (word replacement, upvote/downvote) and sent to the Replika bot.
* **Response Handling**: The bot's responses are retrieved, processed if necessary, and sent back through the WebSocket.

---

### Typical Use Cases

* Controlling chatbots in group chats.
* Automated moderation or fun features in chat groups.
* Integrating a Replika bot into other chat systems via WebSocket.

---

### Conclusion

The script acts as a **bridge** between a local chat infrastructure (WebSocket) and the Replika bot in the browser. It automates communication, can filter messages, and responds to control commands for various operating modes.
