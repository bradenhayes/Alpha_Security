# Run this script after cloning SecurityCameraRPi to install dependancies and build the code

# Helpful links:
# https://prabhatsharma.in/blog/stream-video-from-raspberry-pi/
# https://martinbuberl.com/blog/stream-from-raspberry-pi-to-amazon-kinesis/

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install cmake
sudo apt-get install byacc flex
sudo apt-get install openjdk-8-jdk

#Ensure that JAVA_HOME variable is set and create cert.pem file
#See martinbuberl blog for details...

sudo apt-get install libssl-dev libcurl4-openssl-dev liblog4cplus-1.1-9 liblog4cplus-dev
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-omx

#Set up kvssink
export LD_LIBRARY_PATH=/home/pi/Downloads/amazon-kinesis-video-streams-producer-sdk-cpp/kinesis-video-native-build/downloads/local/lib:$LD_LIBRARY_PATH
export GST_PLUGIN_PATH=/home/pi/Downloads/amazon-kinesis-video-streams-producer-sdk-cpp/kinesis-video-native-build/downloads/local/lib:$GST_PLUGIN_PATH

#export AWS_ACCESS_KEY_ID=AKIAVMRNWFLTQ7RTPWOQ
#export AWS_SECRET_ACCESS_KEY=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
