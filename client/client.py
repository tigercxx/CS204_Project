from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def create_job(quic_enabled, link):
    # Options for Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--remote-debugging-port=9222')

    if not quic_enabled:
        chrome_options.add_argument("disable-quic")

    # Create Driver Instance
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Enable Network domain.
    driver.execute_cdp_cmd('Network.enable', {})

    # Start monitoring network events.
    events = []

    # Define a listener.
    def event_listener(event):
        if event['method'] == 'Network.responseReceived':
            events.append(event)

    # Add the listener.
    driver.command_executor._commands["addListener"] = ("POST", "/session/$sessionId/chromium/connect/networkEvents")
    driver.execute("addListener", {"webSocketUrl": driver.capabilities["goog:chromeOptions"]["debuggerAddress"]})

    # Navigate to the URL
    start = time.time()
    driver.get(link)
    end = time.time()

    # Find the responseReceived event for the main document.
    response_event = next((e for e in events if 'url' in e['params']['response'] and e['params']['response']['url'] == link), None)
    
    if response_event:
        headers = response_event['params']['response']['headers']
        protocol = response_event['params']['response']['protocol']

        # Print headers and protocol
        print("Headers:", headers)
        print("Protocol:", protocol)

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

def main():
    link = "https://localhost:2016"

    with open("exception_log.txt", "w") as exception_log_file:
        for quick_enabled in [False, True]:
            for i in range(1, 5):
                try:
                    time_taken = create_job(quick_enabled, link)
                    # Reduce the number of decimal places
                    time_taken = round(time_taken, 2)

                    print(f"Job {i}:")
                    print(f"QUIC Enabled: {quick_enabled}")
                    print(f"Time taken: {time_taken} seconds")
                    print()                    
                    
                    # Write to CSV
                    log_to_csv("results.csv", [quick_enabled, time_taken])
                except Exception as e:
                    log_exception(exception_log_file, i, e)

if __name__ == "__main__":
    main()
