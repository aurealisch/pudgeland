package me.aurealisch.pudgeland;

import jakarta.websocket.OnMessage;
import jakarta.websocket.OnClose;
import jakarta.websocket.OnOpen;
import jakarta.websocket.Session;
import jakarta.websocket.ClientEndpoint;
import jakarta.websocket.WebSocketContainer;
import jakarta.websocket.ContainerProvider;

import java.net.URI;

@ClientEndpoint
public class WebSocketClientEndpoint {
    private final Pudgeland pudgeland;

    Session session = null;

    public WebSocketClientEndpoint(Pudgeland pudgeland) {
        this.pudgeland = pudgeland;

        WebSocketContainer webSocketContainer = ContainerProvider.getWebSocketContainer();

        try {
            webSocketContainer.connectToServer(this, URI.create("ws://pudgeland-websocket.onrender.com"));
        } catch (Exception exception) {
            this.pudgeland.logger.info("Failed to connect to the websocket server");
        }
    }

    @OnOpen
    public void onOpen(Session session) {
        this.session = session;

        this.pudgeland.logger.info("Opening websocket");
    }

    @OnClose
    public void onClose() {
        this.session = null;

        this.pudgeland.logger.info("Closing websocket");
    }

    @OnMessage
    public void onMessage(String message) {
        this.pudgeland.logger.info("New message from websocket: " + message);
    }
}
