#!/usr/bin/env python3

from typing import Tuple, Dict, List, Union
from validation import *

def parse(filepath: str):
    """
    placeholder
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
            
            curvalidation = validate_questiontype(curline)

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
        
        result = {
            "filename": file_name,
            "questions": dictlist
        }

        print(result)

        return result



def __parse_zaokruzi(lines: List[str], line_counter: int) -> Tuple[int, Dict[str, Union[str, List[str]]]]:
    "Parses a 'zaokruzi' question"
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

        nvalidation: Tuple[bool, bool, str] = validate_zaokruzi_answer(nline)
        
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
    "Parses a 'da-ne' question"
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

def __parse_dopuni(lines: List[str], line_counter: int) -> Tuple[int, Dict[str, Union[str, List[Dict[str, List[str]]]]]]:
    """
    placeholder
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

        nvalidation: Tuple[bool, str, str] = validate_dopuni_answer(nline)

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
            


if __name__ == "__main__":
    parse("test.ptj")