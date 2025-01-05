#Made By mirac-s GitHub
import time
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

print("PLEASE WAIT...")
print("   ")

dns_servers = {
    "8.8.8.8": "Google Public DNS",
    "8.8.4.4": "Google Public DNS",
    "1.1.1.1": "Cloudflare DNS",
    "1.0.0.1": "Cloudflare DNS",
    "208.67.222.222": "OpenDNS",
    "208.67.220.220": "OpenDNS",
    "9.9.9.9": "Quad9 DNS",
    "64.6.64.6": "Verisign DNS",
    "64.6.65.6": "Verisign DNS",
    "4.2.2.1": "Level 3 DNS",
    "4.2.2.2": "Level 3 DNS",
    "94.140.14.14": "AdGuard DNS",
    "94.140.15.15": "AdGuard DNS",
    "185.216.33.241": "Mullvad DNS",
    "185.216.33.242": "Mullvad DNS",
}

# DNS sağlayıcılarına atanacak harfler
dns_details = {
    'a': "Google DNS is known for its speed and reliability.",
    'b': "Cloudflare DNS offers high privacy and performance.",
    'c': "OpenDNS provides strong security and parental control features.",
    'd': "Quad9 DNS blocks malicious domains by default.",
    'e': "Verisign DNS focuses on stability and security.",
    'f': "Level 3 DNS is a reliable, widely-used service.",
    'g': "AdGuard DNS blocks ads, trackers, and provides enhanced security.",
    'h': "Mullvad DNS provides privacy and security with a no-logs policy.",
}

unique_dns_servers = {}
seen_providers = set()
dns_mapping = {} 

for index, (ip, provider) in enumerate(dns_servers.items()):
    if provider not in seen_providers:
        unique_dns_servers[ip] = provider
        seen_providers.add(provider)
        dns_mapping[chr(97 + index)] = (ip, provider)  

def ping_dns(dns_server, provider):
    response_times = []
    for _ in range(5):
        response = ping(dns_server)
        if response is not None:
            response_times.append(round(response, 2))
    if response_times:
        average_response = sum(response_times) / len(response_times)
        return (dns_server, provider, round(average_response, 2))
    else:
        return (dns_server, provider, None)

def batch_ping():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda dns: ping_dns(dns[0], dns[1]), unique_dns_servers.items()))
    
    sorted_results = sorted(results, key=lambda x: (x[2] if x[2] is not None else float('inf')))
    
    for index, (dns_server, provider, response_time) in enumerate(sorted_results, 1):
        if response_time is None:
            print(f"{index:2}. {provider:<18}: Unreachable")
        else:
            
            letter = [k for k, v in dns_mapping.items() if v[1] == provider][0]
            print(f"{index:2}. {provider:<18}: {response_time:5.2f} ms  [{letter}]")


def provider_info():
    while True:
        choice = input("\nEnter the letter of the DNS provider for more details (or 'q' to quit): ").strip().lower()
        if choice == 'q':
            print("Returning to main menu...")
            break
        if choice in dns_details:
            print(f"\nDetails about {dns_mapping[choice][1]}:\n{dns_details[choice]}")
        else:
            print("Invalid choice. Please try again.")

def run():
    while True:
        batch_ping()
        provider_info()
        again = input('\nType "again" to Run Again / Type "f" to End the Program: ').strip().lower()
        if again == "f":
            print("Exiting...")
            break
        elif again != "again":
            print("Invalid input. Please type 'again' or 'f'.")

if __name__ == "__main__":
    run()