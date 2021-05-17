"""Support for the Google Assistant TTS speech service."""
import logging
import requests
import ffmpeg
import voluptuous as vol
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_IP = "ip"
CONF_PORT = "port"

DEFAULT_LANG = "Google-US-English"
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT =  '3000'

SUPPORTED_LANGUAGES = ['Google-US-English']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_IP, default=DEFAULT_IP): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up Google speech component."""
    return GoogleProvider(
        config[CONF_LANG],
        config[CONF_IP],
        config[CONF_PORT],
    )


class GoogleProvider(Provider):
    """The Google TTS API provider."""

    def __init__(self, lang, ip, port):
        """Initialize Google TTS provider."""
        self._lang = lang
        self._ip = ip
        self._port = port
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
            r = requests.post('http://' + self._ip + ':' + self._port + '/assistant',  data = {'command':'repeat after me ' + message})
            audio_url = ('http://' + self._ip + ':' + self._port + r.json()["audio"])
            out, _ = (ffmpeg
                .input(audio_url)
                .output('-', format='mp3', ss=0.566)
                .overwrite_output()
                .run(capture_stdout=True)
            )
        except Exception as e:
            _LOGGER.error("Error while to convert: %s", str(e))
            return (None, None)
        return ("mp3", out)
