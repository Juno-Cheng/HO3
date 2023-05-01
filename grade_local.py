#!/usr/bin/env python3

"""
Do a local practice grading.
The score you recieve here is not an actual score,
but gives you an idea on how prepared you are to submit to the autograder.
"""

import json
import os
import sys

import pandas

import cse40.question
import cse40.assignment
import cse40.style
import cse40.utils

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = os.path.join(THIS_DIR, 'cia_world_factbook_2022.json')

class T1A(cse40.question.Question):
    def score_question(self, submission, world_data):
        result = submission.drop_sparse_columns(world_data, 0.50)
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        self.full_credit()

class T1B(cse40.question.Question):
    def score_question(self, submission, world_data):
        result = submission.extract_numbers(world_data, ['Country', 'Export commodities'])
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        self.full_credit()

class T1C(cse40.question.Question):
    def score_question(self, submission, world_data):
        result = submission.guess_types(world_data)
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        self.full_credit()

class T2A(cse40.question.Question):
    def score_question(self, submission, world_data):
        frame = pandas.DataFrame({'Label': ['1', '2', '3', '4'], 'A': [1.0, 1.5, 2.0, 100.0]})

        result = submission.find_outliers(frame, 1.0, 'Label')
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, dict)):
            self.fail("Answer must be a dict.")
            return

        if (len(result) == 0):
            self.fail("Could not find any outliers.")
            return

        key = list(result.keys())[0]
        if (len(result[key]) == 0):
            self.fail("Got an outlier list that is empty.")
            return

        if (not isinstance(result[key][0], tuple)):
            self.fail("List values should be tuples.")
            return

        if (len(result[key][0]) != 2):
            self.fail("List values should be tuples of length 2.")
            return

        self.full_credit()

class T2B(cse40.question.Question):
    def score_question(self, submission, world_data):
        columns = ['Unemployment rate 2019', 'Unemployment rate 2020', 'Unemployment rate 2021']
        result = submission.merge_columns(world_data, columns, 'Recent Unemployment')
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        self.full_credit()

class T3A(cse40.question.Question):
    def score_question(self, submission, world_data):
        result = submission.one_hot(world_data, 'Export commodities')
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        if ((list(result.columns) == list(world_data.columns)) and (result == world_data)):
            self.fail("Answer should be a NEW DataFrame.")
            return

        self.full_credit()

class T4A(cse40.question.Question):
    def score_question(self, submission, world_data):
        lhs = pandas.DataFrame({'ID': [0, 1, 2], 'A': [1, 2, 3]})
        rhs = pandas.DataFrame({'B': [4, 5, 6]})

        result = submission.left_join(lhs, rhs, ['ID'])
        if (self.check_not_implemented(result)):
            return

        if (not isinstance(result, pandas.DataFrame)):
            self.fail("Answer must be a DataFrame.")
            return

        if (((list(result.columns) == list(lhs.columns)) and (result == lhs))
                or ((list(result.columns) == list(rhs.columns)) and (result == rhs))):
            self.fail("Answer should be a NEW DataFrame.")
            return

        self.full_credit()

def grade(path):
    submission = cse40.utils.prepare_submission(path)

    with open(DATA_PATH, 'r') as file:
        data = json.load(file)

    world_data = pandas.DataFrame.from_dict(data, orient = 'index')
    world_data.sort_index(axis = 0, inplace = True)
    world_data.insert(0, 'Country', world_data.index)
    world_data.reset_index(drop = True, inplace = True)

    additional_data = {
        'world_data': world_data,
    }

    questions = [
        T1A("Task 1.A (drop_sparse_columns)", 1),
        T1B("Task 1.B (extract_numbers)", 1),
        T1C("Task 1.C (guess_types)", 1),
        T2A("Task 2.A (find_outliers)", 1),
        T2B("Task 2.B (merge_columns)", 1),
        T3A("Task 3.A (one_hot)", 1),
        T4A("Task 4.A (left_join)", 1),
        cse40.style.Style(path, max_points = 1),
    ]

    assignment = cse40.assignment.Assignment('Practice Grading for Hands-On 3', questions)
    assignment.grade(submission, additional_data = additional_data)

    return assignment

def main(path):
    assignment = grade(path)
    print(assignment.report())

def _load_args(args):
    exe = args.pop(0)
    if (len(args) != 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <submission path (.py or .ipynb)>" % (exe), file = sys.stderr)
        sys.exit(1)

    path = os.path.abspath(args.pop(0))

    return path

if (__name__ == '__main__'):
    main(_load_args(list(sys.argv)))
