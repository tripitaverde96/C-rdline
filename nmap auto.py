import nmap

scanner = nmap.PortScanner()

ip = input("Inserte una direccion IP")
print("Esta es la Ip que escribiste:", ip)
scanner.scan(ip)

print(scanner.all_hosts())
