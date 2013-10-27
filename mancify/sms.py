from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import re
import logging

from clockwork import clockwork


# Maximum length of an SMS message (with triple concatenation, the maximum
# permitted under GSM)
SMS_MAX_LENGTH = 459


class MancifySMSService(object):
    def __init__(self, api_key):
        self.api = clockwork.API(api_key)

    def send(self, sender, recipient, content):
        logging.debug('Sending message to %s', recipient)
        for chunk in self.format(content):
            # Send up to 459 characters at a time (the maximum length of a
            # triple concatenated SMS message)
            msg = clockwork.SMS(to=recipient, from_name=sender, message=chunk)
            response = self.api.send(msg)
            if not response.success:
                logging.error('%s %s', response.error_code, response.error_description)

    def format(self, content):
        # Replace multiple consecutive spaces and line breaks with individual
        # spaces and line breaks (no sense wasting credits on them)
        content = content.strip()
        content = re.sub(' +', ' ', content)
        content = re.sub('\r\n', '\n', content)
        content = re.sub('\n+', '\n', content)
        # If necessary, chunk content into SMS_MAX_LENGTH chunks, prefixing
        # each with a page number
        if len(content) < SMS_MAX_LENGTH:
            yield content
        else:
            sent = 0
            page = 1
            while content and sent < self.output_limit:
                content = 'p%d:\n%s' % (page, content.strip())
                if (sent + SMS_MAX_LENGTH) > self.output_limit:
                    chunk = content[:SMS_MAX_LENGTH - 3] + '...'
                    content = ''
                elif len(content) < SMS_MAX_LENGTH:
                    chunk = content
                    content = ''
                else:
                    # Try and split on a line break or a space if one is near
                    # the end of the current chunk
                    match = re.match('(.*)[ \n](.*)', content[:SMS_MAX_LENGTH], re.DOTALL)
                    if match and len(match.group(2)) < 10:
                        chunk = match.group(1)
                        content = match.group(2) + content[SMS_MAX_LENGTH:]
                    else:
                        chunk = content[:SMS_MAX_LENGTH]
                        content = content[SMS_MAX_LENGTH:]
                yield chunk
                sent += len(chunk)
                page += 1

