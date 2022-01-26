#!/usr/bin/pyton

import argparse
import sys
import csv

parser = argparse.ArgumentParser(description='Script to extract motor output PWM from ardupilot flight logs.')

parser.add_argument("-i", "--input_file", help="Input file. Should be a .log file from ardupilot flight controller")
parser.add_argument("-o", "--output_file", help="Output file. Should be a csv at the location you want the output file")
parser.add_argument("-n", "--num_motors", help="Number of motors you would like to extract, defaults = 4", default=4)
parser.add_argument("-v", "--verbose", help="Whether you would like to print all of the output WARNING prints entire generated file to console, defaults = False", default=False)

arguments = parser.parse_args()

if len(sys.argv) == 1:
   parser.print_help()
   exit()
elif arguments.input_file == None:
   print("Please include an input file in the arguments!")
   print("Use -i or --input_file")
   exit()
elif arguments.output_file == None:
   print("Please include an output file in the arguments!")
   print("Use -o or --output_file")
   exit()
else:
   input_file = arguments.input_file
   output_file = arguments.output_file
   num_motors = arguments.num_motors
   verbose = arguments.verbose

time = []
motor1 = []
motor2 = []
motor3 = []
motor4 = []

try:
   # opening file and saving time and motor pwm
   with open(input_file, 'r') as file:
      reader = csv.reader(file, delimiter = ',')
      for row in reader:
         if(row[0] == "RCOU"):
               try:
                  time.append(float(row[1]) * (10 ** -6))
                  motor1.append(int(row[2]))
                  motor2.append(int(row[3]))
                  motor3.append(int(row[4]))
                  motor4.append(int(row[5]))
               except EnvironmentError:
                  print("There was an error reading the input file, please make sure that it is formatted correctly.")
                  exit()
except EnvironmentError:
   print("Couldn't open the input file, please make sure you are using the correct file. Exiting the script....")
   exit()

if(verbose):
    for i in range(len(time)):
        print("time: %f - motor1: %d motor2: %d motor3: %d motor4: %d" % (time[i], motor1[i], motor2[i], motor3[i], motor4[i]))

try:
   # open file and writing the time and motor pwm output
   with open(output_file, 'w', encoding='UTF8', newline='') as f:
      # create the csv writer
      writer = csv.writer(f)

      writer.writerow(["time", "motor1", "motor2", "motor3", "motor4"])
      rows = len(time)
      for i in range(0, rows):

         row = [time[i] - time[0], motor1[i], motor2[i], motor3[i], motor4[i]]

         # write a row to the csv file
         writer.writerow(row)
except EnvironmentError:
   print("Couldn't open the output file, please make sure you are using the correct file. Exiting the script....")
   exit()

print("The pwm from %d motors has successfully been extracted from %s and written to %s" % (num_motors, input_file, output_file))