from webserver import TopologyWebServer

def main():
    # Define the path to your Neox YAML configuration file.
    config_filepath = "20B.yml"
    
    # Create an instance of the TopologyWebServer.
    server = TopologyWebServer(config_filepath=config_filepath, total_gpus=96, host='0.0.0.0', port=5000)
    
    # Start the web server.
    server.run()

if __name__ == "__main__":
    main()
