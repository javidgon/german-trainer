import sys
import csv
import time
from random import shuffle, choice, randint


def ask_questions(translations):
    def _throw_questions(key, present, perfekt, points, failures):
        result_present = raw_input("[V] Could you please write the German translation of '{}': ".format(key))
        if result_present == present:
            points += 5
            print ":) Awesome!\n"
            result_perfekt = raw_input("[V] And the PERFEKT form? (for the first person of singular 'ich'): ")
            if result_perfekt == perfekt:
                points += 10
                print ":) You are a master!\n"
            else:
                points -= 5
                print ":( Damn! The right answer is '{}'\n".format(perfekt)
        else:
            points -= 10
            failures.append(key)
            print ":( I hate german! The right answer is '{}'\n".format(present)
        print "[I] You currently have {} points\n".format(str(points))
        return points

    points = 0
    failures = []
    keys = [k for k in translations]
    shuffle(keys)  
    for key in keys:
        present = translations[key][0]
        perfekt = translations[key][1]
        points = _throw_questions(key, present, perfekt, points, failures)
        # Sometimes is good to try again with failures
        refresh_failure = True if randint(1, 5) == 4 else False
        if refresh_failure:
           points =  _throw_questions(choice(failures), present, perfekt, points, failures)
        # is it time to stop? 
        should_stop = True if randint(1, 3) == 2 else False
        if should_stop:
            print "See you in 5 minutes!"
            time.sleep(60*5)


def associate_translations(filename):
  translations = {}
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    counter = 0
    for row in reader:
      if counter > 0:
        translations[row[2]] = [row[0], row[1]]
      counter += 1
  return translations


if __name__ == '__main__':
  print "*******************************************************"
  print "*                  VERBS TRAINER"
  print "*******************************************************"
  filename = sys.argv[1]
  print "Building translations...\n"
  translations = associate_translations(filename)
  print "Asking questions...\n"
  ask_questions(translations)
