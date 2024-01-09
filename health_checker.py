import yaml # pip install pyYAML
import sys
import time
import requests

endpointsInfo = []
domain_stats = {}

def parse_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)

        for endpoint in data:
        	endpoint['success'] = 0
        	endpointsInfo.append(endpoint)

def check_endpoint_status(endpoint):
    try:
        start_time = time.time()
        response = requests.request(endpoint.get('method', 'GET'), endpoint['url'], headers=endpoint.get('headers', {}), data=endpoint.get('body', ''))
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if 200 <= response.status_code < 300 and latency < 500:
            return 1
        else:
            return 0
    except requests.exceptions.RequestException:
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <yaml_file_path>")
        sys.exit(1)

    yaml_path = sys.argv[1]
    parse_yaml(yaml_path)
    total_calls = 0

    try:
        while True:
            total_calls += 1
            print("\nChecking endpoints:")
            for endpoint in endpointsInfo:
            	status = check_endpoint_status(endpoint)
            	domain = endpoint['url'].split('//')[1].split('/')[0]
            	domain_stats.setdefault(domain, {'success': 0, 'total': 0})
            	domain_stats[domain]['total'] += 1
            	domain_stats[domain]['success'] += status

            for domain, stats in domain_stats.items():
                availability_percentage = round((stats['success'] / stats['total']) * 100)
                print(f"{domain} has {availability_percentage}% availability percentage")

            time.sleep(15)
    except KeyboardInterrupt:
        print("Exiting the program.")
