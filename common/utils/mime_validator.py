import magic
from pathlib import Path
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileMimeValidator:

    messages = {
        "malicious": "File looks malicious. Allowed extensions are: '%(allowed_extensions)s'.",
        "not_supported": "File extension '%(extension)s' is not allowed. "
                         "Allowed extensions are: '%(allowed_extensions)s'."
    }

    code = "invalid_extension"
    ext_cnt_mapping = {
        "IMAGE": {
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'jpg': 'image/jpeg'
        },
        "AUDIO": {
            'mp3': "audio/mpeg",
            'wav': "audio/wav"
        },
        "VIDEO": {
            'mp4': "video/mp4"
        }
    }

    def __init__(self, type):
        self.type = type
        self.allowed_extensions = [allowed_extension.lower(
        ) for allowed_extension in self.ext_cnt_mapping[type].keys()]

    def __call__(self, data):
        extension = Path(data.name).suffix[1:].lower()
        content_type = magic.from_buffer(data.read(2048), mime=True)
        if extension not in self.allowed_extensions:
            raise ValidationError(
                self.messages['not_supported'],
                code=self.code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )
        if content_type != self.ext_cnt_mapping[self.type][extension]:
            raise ValidationError(
                self.messages['malicious'],
                code=self.code,
                params={
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_extensions == other.allowed_extensions and
            self.message == other.message and
            self.code == other.code
        )
