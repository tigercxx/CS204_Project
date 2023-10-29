import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def set_network_conditions(driver, offline=False, latency=0, download_throughput=0, upload_throughput=0):
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})  # Disable cache
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        'offline': offline,
        'latency': latency,  # additional latency (ms)
        'downloadThroughput': download_throughput,  # max download throughput (bytes/s)
        'uploadThroughput': upload_throughput  # max upload throughput (bytes/s)
    })



def create_job(protocol, link):
    # Options for Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--remote-debugging-port=9222')

    if protocol == "http1.1":
        chrome_options.add_argument("--disable-quic")
        chrome_options.add_argument("--disable-http2")
    elif protocol == "http2":
        chrome_options.add_argument("--disable-quic")
    elif protocol == "http3":
        chrome_options.add_argument("--enable-quic")
        domain_port = link.split("//")[1]
        chrome_options.add_argument("--origin-to-force-quic-on=" + domain_port)

    # Create Driver Instance
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # set_network_conditions(driver, latency=100, download_throughput=1000 * 1024, upload_throughput=1000 * 1024)  


    # Navigate to the URL
    start = time.time()
    driver.get(link)
    end = time.time()

    # Quit the driver
    driver.quit()

    return end - start


def log_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

def log_exception(exception_log_file, job_number, e):
    error_message = f"An error occurred in Job {job_number}: {str(e)}"
    print(error_message)
    exception_log_file.write(error_message + "\n")

def main(iterations, url):
    URL = url if url else "https://google.com"
    ITERATIONS = iterations if iterations > 0 else 1
    PROTOCOLS = ["http1.1", "http2", "http3"]
    DOMAIN = URL.split("//")[1].split("/")[0]

    # Clear data in CSV files
    for protocol in PROTOCOLS:
        with open(f"data/{protocol}_{DOMAIN}.csv", 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["time_taken"])
            csvfile.close()

    for protocol in PROTOCOLS:
        for i in range(ITERATIONS):
            try:
                time_taken = create_job(protocol, URL)
                time_taken = round(time_taken, 2)

                print(f"Job {i + 1}:")
                print(f"Protocol: {protocol}")
                print(f"Time taken: {time_taken} seconds")
                print()                    

                # Write to CSV
                log_to_csv(f"data/{protocol}_{DOMAIN}.csv", [time_taken])
            except Exception as e:
                log_exception("exception_log.txt", i + 1, e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure page load time with http1.1, http2, http3.")
    parser.add_argument("iterations", type=int, help="Number of iterations to run.")
    parser.add_argument("url", type=str, help="Web page link to measure.")
    
    args = parser.parse_args()

    if not args.url:
        print("URL not provided, using https://google.com")

    if args.iterations < 1:
        print("Iterations must be greater than 0.")
        exit(1)

    if not args.iterations:
        print("Iterations not provided, using 1.")

    if not args.url.startswith("http"):
        print("URL must start with http or https.")
        exit(1)

    main(args.iterations, args.url)
