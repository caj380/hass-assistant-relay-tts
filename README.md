
# Google Assistant TTS for Home Assistant

This is a custom component to allow Home Assistant to use the much more realistic Google Assistant text-to-speech voice.

It requires an [Assistant Relay v3](https://assistantrelay.com/) server to be running and accessible from your Home Assistant device.

[Apipa169](https://github.com/Apipa169)  made a great Assistant Relay add-on for Hassio available [here](https://github.com/Apipa169/Assistant-Relay-for-Hassio)

## Installation
This component is available via HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) which is the recommended method of installation. 

You can also copy `custom_components/google_assistant_tts` to your `custom_components` folder in HomeAssistant if you prefer to install manually.

## Example `tts` entry in your `configuration.yaml`

    # Text to speech
    tts:
      - platform: google_assistant_tts
        #Assistant Relay Server IP
        ip: "127.0.0.1"
        #Assistant Relay Server port
        port: "3000"
