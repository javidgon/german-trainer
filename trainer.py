import sys
import os
import csv
import time
import requests
import json

from random import shuffle, choice, randint


BOT_TOKEN = os.getenv('BOT_TOKEN')
URL = 'https://api.telegram.org/bot{}'.format(BOT_TOKEN)
DEFAULT_MODE = 'verben'

def ask_questions(verbs_translations, words_translations, mode):
    def _fetch_updates():
        res = requests.get(URL + '/getUpdates')
        content = json.loads(res.content).get('result')
        chat_id = content[-1].get('message').get('chat').get('id')
        timestamp = content[-1].get('message').get('date')
        result = content[-1].get('message').get('text')
        return chat_id, timestamp, result

    def _send_question(text, chat_id):
        res = requests.get(URL + '/sendMessage?text={}&chat_id={}'.format(text, chat_id))

    def _throw_questions(key, translation, failures, mode):
        chat_id = None
        timestamp = None
        result = None
        new_timestamp = None

        while not timestamp:
            chat_id, timestamp, result = _fetch_updates()

        # This only occurs the first time.
        if not mode:
            _send_question('Welcome to the German trainer!', chat_id)
            _send_question('You can change categories by typing: /words or /verbs.', chat_id)
            _send_question('When answering questions about verbs, please use the following structure: e.g "trennen, habe getrennt". Enjoy!', chat_id)
            return DEFAULT_MODE

        if mode == 'verben':
            _send_question('Could you please write the present and perfekt forms of the verb: "{}"?'.format(key), chat_id)
        else:
            _send_question('Could you please write the german translation of the name: "{}"?'.format(key), chat_id)

        new_timestamp = timestamp
        while timestamp == new_timestamp:
            time.sleep(5)
            chat_id, new_timestamp, result = _fetch_updates()

        if result == '/words':
            return 'worter'
        elif result == '/verbs':
            return 'verben'

        if result.lower() == '{}'.format(translation):
            _send_question(':) Awesome!', chat_id)
            if key in failures:
                failures.remove(key)
        else:
            _send_question(':( Damn! The right answer is "{}"'.format(translation), chat_id)
            failures.append(key)
        return mode


    failures = []
    verbs_keys = [k for k in verbs_translations]
    words_keys = [k for k in words_translations]
    shuffle(verbs_keys)
    shuffle(words_keys)
    keys = verbs_keys if mode == 'verben' or mode is None else words_keys
    for key in keys:
        if mode == 'verben' or mode is None:
            present = verbs_translations[key][0]
            perfekt = verbs_translations[key][1]
            translation = '{}, {}'.format(present, perfekt)
        else:
            translation = words_translations[key]

        mode = _throw_questions(key, translation, failures, mode)
        if mode in ['worter', 'verben']:
            return mode

        # Sometimes is good to try again with failures
        refresh_failure = True if randint(1, 5) == 4 else False
        if refresh_failure and len(failures) > 0:
            _throw_questions(choice(failures), translation, failures, mode)
    return mode


def associate_verbs(filename):
  translations = {}
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    counter = 0
    for row in reader:
      if counter > 0:
        translations[row[2]] = [row[0].lower(), row[1].lower()]
      counter += 1
  return translations


def associate_words(filename):
  translations = {}
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    counter = 0
    for row in reader:
      if counter > 0:
        translations[row[1]] = row[0].lower()
      counter += 1
  return translations


if __name__ == '__main__':
  print "*******************************************************"
  print "*                  GERMAN TRAINER"
  print "*******************************************************"
  if not BOT_TOKEN:
      print 'Error: BOT_TOKEN env var not set'
      sys.exit(1)
  filename_verbs = sys.argv[1]
  filename_words = sys.argv[2]
  print "Building translations...\n"
  verbs_translations = associate_verbs(filename_verbs)
  words_translations = associate_words(filename_words)
  print "Asking questions...\n"
  selected_mode = None
  while True:
    selected_mode = ask_questions(verbs_translations, words_translations, selected_mode)
    selected_mode = selected_mode if selected_mode else DEFAULT_MODE
