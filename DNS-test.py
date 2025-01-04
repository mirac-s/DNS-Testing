import time
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

print("Please wait...")
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
}

unique_dns_servers = {}

seen_providers = set()

for ip, provider in dns_servers.items():
    if provider not in seen_providers:
        unique_dns_servers[ip] = provider
        seen_providers.add(provider)

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
    
    best_dns = None
    best_ping = float('inf')

    for index, (dns_server, provider, response_time) in enumerate(sorted_results, 1):
        if response_time is None:
            print(f"{index:2}. {provider:<18}: Unreachable")
        else:
            print(f"{index:2}. {provider:<18}: {response_time:5.2f} ms")
            if response_time < best_ping:
                best_ping = response_time
                best_dns = (dns_server, provider)

    if best_dns:
        print(f"\n#Best DNS Server: {best_dns[1]} ({best_dns[0]}) with an average ping of {best_ping:.2f} ms")

def run():
    while True:
        batch_ping()
        again = input('\nType "a" to Run Again / Type "f" to End the Program: ').strip().lower()
        if again != "a":
            print("Exiting...")
            break

if __name__ == "__main__":
    run()