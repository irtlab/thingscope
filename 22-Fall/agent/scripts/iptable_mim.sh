iptables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 443 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 1883 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i wlp4s0 -p tcp --dport 8883 -j REDIRECT --to-port 8080
