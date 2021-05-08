"""Support for the Google Assistant TTS speech service."""
import logging
import requests
import voluptuous as vol
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PITCH = "pitch"
CONF_BITRATE = "bitrate"

DEFAULT_LANG = "Google-US-English"
DEFAULT_PITCH = "100"
DEFAULT_BITRATE = "128k"

SUPPORTED_LANGUAGES = ['Google-US-English']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): cv.string,
        vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): cv.string,
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up Google speech component."""
    return GoogleProvider(
        config[CONF_LANG],
        config[CONF_PITCH],
        config[CONF_BITRATE],
    )


class GoogleProvider(Provider):
    """The Google TTS API provider."""

    def __init__(self, lang, pitch, bitrate):
        """Initialize Google TTS provider."""
        self._lang = lang
        self._pitch = pitch
        self._bitrate = bitrate
        self.name = "GoogleTTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORTED_LANGUAGES

    def get_tts_audio(self, message, language, options=None):
        """Load TTS using requests."""
        if language is None:
            language = self._lang
        try:
            r = requests.get('http://192.168.1.105:4000/tts?text=' + message)
            #convert = pyttsreverso.ReversoTTS()
            #data = convert.convert_text(voice=language, pitch=self._pitch, bitrate=self._bitrate, msg=message)
        except Exception as e:
            _LOGGER.error("Error while to convert: %s", str(e))
            return (None, None)
        return ("mp3", r.content)
