# ft_onion

ssh -p 4242 -o ProxyCommand="nc -X 5 -x 127.0.0.1:9150 %h %p" -o "ServerAliveInterval 60" user@onion-address.onion

-p 4242:
    Specifies the SSH port
-o ProxyCommand="nc -X 5 -x 127.0.0.1:9150 %h %p":
    Redirects SSH traffic through Tor by using the SOCKS5 proxy on port 9150
-o "ServerAliveInterval 60":
    Keeps the connection alive by sending periodic messages to the server
user@onion-adress.onion:
    Connects to the specified .onion address as the user