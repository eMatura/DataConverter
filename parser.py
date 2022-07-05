#!/usr/bin/env python3

from typing import Tuple, Dict, List, Union
from validation import *

def parse(filepath: str):
    """
    Attempts to parse an entire Pitanja file.

    It first checks whether the file starts with a Pitanja signature ('@PITANJA_FILE <name>').
    It extracts the file name from this signature.
    
    Then it iterates over the file line by line and attempts to parse question by question.

    Whenever it encounters a question signature ('@PITANJE <type>') it moves to the next line and calls the
    appropriate parser method which parses the rest of the question until the question end signature ('---===---').

    Once it finishes, it returns a dictionary object containing the file name and a list of all parsed questions.
    """
    with open(filepath, "r") as pitanja_file:

        pitanja_lines = pitanja_file.readlines()

        file_validation = validate_file(pitanja_lines[0])
        file_name: str = ""
        dictlist = []

        if not file_validation[0]:
            raise Exception("Could not begin parsing! Invalid file passed.")
        else:
            file_name = file_validation[1]
        
        cur_counter = 1
        pitanja_size = len(pitanja_lines)


        while cur_counter < pitanja_size:
            curline: str = pitanja_lines[cur_counter]

            if curline.isspace():
                cur_counter += 1
                continue
            
            curvalidation: Tuple[bool, str] = validate_questiontype(curline)

            if not curvalidation[0]:
                raise Exception("Provided invalid question type line: ", curline)
            else:
                if curvalidation[1] == "zaokruzi":
                    res = __parse_zaokruzi(pitanja_lines, (cur_counter + 1))
                    dictlist.append(res[1])
                    cur_counter = (res[0] + 1)

                elif curvalidation[1] == "da-ne":
                    res = __parse_dane(pitanja_lines, (cur_counter + 1))
                    dictlist.append(res[1])
                    cur_counter = (res[0] + 1)

                elif curvalidation[1] == "dopuni":
                    res = __parse_dopuni(pitanja_lines, (cur_counter + 1))
                    dictlist.append(res[1])
                    cur_counter = (res[0] + 1)
                    
                else:
                    raise Exception("Invalid question type provided!")
        
        result = {
            "filename": file_name,
            "questions": dictlist
        }

        return result



def __parse_zaokruzi(lines: List[str], line_counter: int) -> Tuple[int, Dict[str, Union[str, List[str]]]]:
    """
    Parses a 'zaokruzi' question by iterating over all lines until reaching the line containing '---===---'.
    Empty lines are ignored.

    The first non-empty line must start with a question signature ('??? <question>') which contains the actual
    question.

    Then the following lines (until question end) must all conform to the form of '@+/- <answer>' where '+' denotes
    a right and '-' denotes a wrong answer.

    Once parsing is finished, it returns a tuple containing: 
    
    - index of question end line

    - dictionary object containing question type ('zaokruzi'), question itself, 
      a list of right answers and a list of wrong answers.
    """

    qline: str = lines[line_counter]
    while qline.isspace():
        line_counter += 1
        qline = lines[line_counter]

    question: str = ""
    qvalidation: Tuple[bool, str] = validate_questionline(qline)

    if not qvalidation[0]:
        raise Exception("Provided invalid question line: ", qline)
    else:
        question = qvalidation[1]

    line_counter += 1
    
    wrongAnswers: List[str] = []
    rightAnswers: List[str] = []

    lineslen = len(lines)

    while line_counter < lineslen:
        nline: str = lines[line_counter]

        if nline.isspace():
            line_counter += 1
            continue

        if nline.strip() == "---===---":
            line_counter += 1
            break
        #                  valid,   right/wrong,    answer
        nvalidation: Tuple[bool,       bool,         str] = validate_zaokruzi_answer(nline)
        
        if not nvalidation[0]:
            raise Exception("Provided invalid answer line: ", nline)
        else:
            if nvalidation[1]:
                rightAnswers.append(nvalidation[2])
            else:
                wrongAnswers.append(nvalidation[2])
        
        line_counter += 1
    
    result = {
        "type": "zaokruzi",
        "question": question,
        "rightAnswers": rightAnswers,
        "wrongAnswers": wrongAnswers
    }

    return (line_counter, result)

def __parse_dane(lines: List[str], line_counter: int) -> Tuple[int, Dict[str, str]]:
    """
    Parses a 'zaokruzi' question by iterating over all lines until reaching the line containing '---===---'.
    Empty lines are ignored.

    The first non-empty line must start with a question signature ('??? <question>') which contains the actual
    question.

    Then the following line must be either '@DA' (denoting "true") or '@NE' (denoting "false"). It assumes only one
    such line will be provided, but in the case of multiple lines being provided (which is itself nonsense) only the content
    of the last line will be returned.

    Once parsing is finished, it returns a tuple containing: 
    
    - index of question end line

    - dictionary object containing question type ('da-ne'), question itself, right answer
    """
    qline: str = lines[line_counter]
    while qline.isspace():
        line_counter += 1
        qline = lines[line_counter]
    
    question: str = ""
    qvalidation: Tuple[bool, str] = validate_questionline(qline)

    if not qvalidation[0]:
        raise Exception("Provided invalid question line: ", qline)
    else:
        question = qvalidation[1]

    line_counter += 1
    
    rightAnswer: str = ""

    lineslen = len(lines)

    while line_counter < lineslen:
        nline: str = lines[line_counter]

        if nline.isspace():
            line_counter += 1
            continue

        if nline.strip() == "---===---":
            line_counter += 1
            break

        nvalidation: Tuple[bool, str] = validate_dane_answer(nline)

        if not nvalidation[0]:
            raise Exception("Provided invalid answer line: ", nline)
        else:
            rightAnswer = nvalidation[1]
        
        line_counter += 1

    result = {
        "type": "da-ne",
        "question": question,
        "rightAnswer": rightAnswer
    }

    return (line_counter, result)

def __parse_dopuni(lines: List[str], line_counter: int) -> Tuple[int, Dict[str, Union[str, Dict[str, List[str]]]]]:
    """
    Parses a 'dopuni' question by iterating over all lines until reaching the line containing '---===---'.
    Empty lines are ignored.

    The first non-empty line must start with a question signature ('??? <question>') which contains the actual
    question.

    Then the following lines (until question end) must all conform to the form of '@<key> <answer>' where the key is some
    string or integer value.
    These are then placed in a dictionary (key is key) where value is a list of strings (all answers tied to a particular key).

    Once parsing is finished, it returns a tuple containing: 
    
    - index of question end line

    - dictionary object containing question type ('dopuni), question itself,
      answer dictionary (keys holding lists of answers)
    """
    qline: str = lines[line_counter]
    while qline.isspace():
        line_counter += 1
        qline = lines[line_counter]
    
    question: str = ""
    qvalidation: Tuple[bool, str] = validate_questionline(qline)

    if not qvalidation[0]:
        raise Exception("Provided invalid question line: ", qline)
    else:
        question = qvalidation[1]

    line_counter += 1
    
    rightAnswers: Dict[str, List[str]] = {}

    lineslen = len(lines)

    while line_counter < lineslen:
        nline: str = lines[line_counter]

        if nline.isspace():
            line_counter += 1
            continue

        if nline.strip() == "---===---":
            line_counter += 1
            break
        #                  valid,   key,   answer    
        nvalidation: Tuple[bool,    str,    str] = validate_dopuni_answer(nline)

        if not nvalidation[0]:
            raise Exception("Provided invalid answer line: ", nline)
        else:
            if nvalidation[1] not in rightAnswers:
                rightAnswers[nvalidation[1]] = []
            
            rightAnswers[nvalidation[1]].append(nvalidation[2])
        
        line_counter += 1
    
    result = {
        "type": "dopuni",
        "question": question,
        "rightAnswers": rightAnswers
    }

    return (line_counter, result)