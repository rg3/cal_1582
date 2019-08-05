#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# COPYRIGHT AND PERMISSION NOTICE
# 
# Copyright (c) 2005,2019 Ricardo Garcia
# 
# All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, and/or sell copies of the Software, and to permit persons 
# to whom the Software is furnished to do so, provided that the above 
# copyright notice(s) and this permission notice appear in all copies of 
# the Software and that both the above copyright notice(s) and this 
# permission notice appear in supporting documentation.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT 
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL 
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING 
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION 
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# 
# Except as contained in this notice, the name of a copyright holder 
# shall not be used in advertising or otherwise to promote the sale, use 
# or other dealings in this Software without prior written authorization 
# of the copyright holder.

import calendar
import sys
import os.path


__all__ = ["gregorian_reformation_year", "gregorian_reformation_month",
	   "gregorian_reformation_step", "gregorian_reformation_month_calendar",
	   "leapdays_function_error", "spaces_per_cell",
	   "previous_leap_days", "is_leap_year", "days_on_month", "days_up_to",
	   "month_calendar", "print_month" ]


#######################
##### Global data #####
#######################


# Establish Gregorian Reformation data
gregorian_reformation_year = 1582	# Year
gregorian_reformation_month = 10	# Month
gregorian_reformation_step = 10		# Step taken (in days)
gregorian_reformation_month_calendar = [[ 1,  2,  3,  4, 15, 16, 17],
				      [18, 19, 20, 21, 22, 23, 24],
				      [25, 26, 27, 28, 29, 30, 31],
				      [ 0,  0,  0,  0,  0,  0,  0],
				      [ 0,  0,  0,  0,  0,  0,  0],
				      [ 0,  0,  0,  0,  0,  0,  0]]


# Constants
ancient_leapyear_period = 4
leapdays_function_error = 12	# See previous_leap_days() for more info.
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday",
		"Friday", "Saturday", "Sunday"]
brief_week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
month_names = ["?", "January", "February", "March", "April", "May", "June",
	       "July", "August", "September", "October", "November", "December"]

# Pretty-printing parameters
spaces_per_cell = 2


#########################################################
##### Module functions based on the calendar module #####
#########################################################


def previous_leap_days(year):
	"""Returns the number of leap years in the range [1, year)."""

	if year <= gregorian_reformation_year:
		return (year - 1) // ancient_leapyear_period
	# calendar.leapdays() calculates always according to the new method,
	# so in the "real world" it's off by 12 years/days when applicable
	return calendar.leapdays(1, year) + leapdays_function_error


def is_leap_year(year):
	"""Returns True if year is a leap year, and False otherwise."""

	if year <= gregorian_reformation_year:	# Old method
		return ((year % ancient_leapyear_period) == 0)
	return calendar.isleap(year)		# New method


def days_on_month(month, year):
	"""Returns the number of days that month has."""

	global month_names
	global month_days
	global gregorian_reformation_month
	global gregorian_reformation_year
	global gregorian_reformation_month_calendar

	if (month == gregorian_reformation_month and
	    year == gregorian_reformation_year):
		# Days in the "special month"
		return sum([sum([x != 0 for x in line]) for line in
			    gregorian_reformation_month_calendar])
	if is_leap_year(year) and month_names[month] == "February":
		return month_days[month] + 1
	return month_days[month]


def days_up_to(month, year):
	"""Returns the number of days in the range [1-1-1, year-month-1)."""

	global month_days
	global month_names
	global gregorian_reformation_year
	global gregorian_reformation_month
	global gregorian_reformation_step

	# This is computed as:
	# 	(year - 1) * 365			+
	# 	leap days up to year			+
	# 	days passed in this year		+
	# 	1 more if leap year and apropiate	-
	# 	reformation step if appropriate
	number_of_days = 0
	number_of_days += (year - 1) * sum(month_days[1:])
	number_of_days += previous_leap_days(year)
	number_of_days += sum(month_days[0:month])
	if (calendar.isleap(year) and
	    month > month_names.index("February")):
		number_of_days += 1
	if (year > gregorian_reformation_year or
	    (year == gregorian_reformation_year and
	     month > gregorian_reformation_month)):
		number_of_days -= gregorian_reformation_step
	return number_of_days


def month_calendar(month, year):
	"""Returns a 6x7 matrix representing the calendar for that month. Empty
	positions are filled with zeros."""

	global gregorian_reformation_month
	global gregorian_reformation_year
	global gregorian_reformation_month_calendar
	global week_days
	global empty_month_calendar

	if (month == gregorian_reformation_month and
	    year == gregorian_reformation_year):
		# Special case
		return gregorian_reformation_month_calendar

	# Calculate the week day number (0-6) of "month 1st, year"
	# based on the days that have passed up to that day and taking into
	# account January 1st, 1 was Saturday
	week_day_number = ((days_up_to(month, year) +
			    week_days.index("Saturday")) %
			   len(week_days))
	# Start with the empty matrix and fill it
	month_calendar = [[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0]]
	row = 0
	column = week_day_number
	for mthday in range(1, days_on_month(month, year) + 1):
		month_calendar[row][column] = mthday
		if column == len(week_days) - 1:
			row += 1
		column = (column + 1) % len(week_days)
	return month_calendar


def print_month(month, year):
	"""Prints the calendar for that month on screen."""

	global month_names
	global week_days
	global spaces_per_cell
	global brief_week_days

	mmat = month_calendar(month, year)

	# Header
	print(((month_names[month] + " " + str(year)).
		center(spaces_per_cell * len(week_days) + len(week_days) - 1)))
	# Column titles
	for name in brief_week_days:
		print(name.rjust(spaces_per_cell), end=' ')
	print()
	# Days matrix
	for row in mmat:
		for day in row:
			if day == 0:
				print(spaces_per_cell * " ", end=' ')
			else:
				print(str(day).rjust(spaces_per_cell), end=' ')
		print()


########################
##### Main program #####
########################


if __name__ == "__main__":
	try:
		month = int(sys.argv[1])
		year = int(sys.argv[2])
		if month < 1 or month > 12 or year < 1:
			raise ValueError
	except (ValueError, IndexError):
		sys.exit("Usage: " + os.path.basename(sys.argv[0]) +
								" month year")
	print_month(month, year)
