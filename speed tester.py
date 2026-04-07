import speedtest

def check_internet_speed():
    try:
        # Create speedtest object
        st = speedtest.Speedtest()
        
        # Get best server
        print("Finding optimal server...")
        st.get_best_server()
        
        # Perform download speed test
        print("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Perform upload speed test
        print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Print results
        print("\n--- Results ---")
        print(f"Download speed: {download_speed:.2f} Mbps")
        print(f"Upload speed: {upload_speed:.2f} Mbps")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_internet_speed()