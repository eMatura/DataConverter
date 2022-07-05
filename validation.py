from typing import Tuple, Dict, List, Union

def validate_file(firstline: str) -> Tuple[bool, str]:
    """
    Ensures the provided file starts with the form '@PITANJA_FILE <name>'
    Returned tuple contains (validation result, name)
    """
    split = firstline.split(" ")

    if len(split) != 2: 
        return (False, "")
    else:
        return (split[0] == "@PITANJA_FILE", split[1])

def validate_questiontype(qtype: str) -> Tuple[bool, str]:
    """
    Ensures the provided question type line conforms to the form '@PITANJE <type>'
    Returned tuple contains (validation result, type)
    """
    split = qtype.split(" ")

    if len(split) != 2: 
        return (False, "")
    else:
        return (split[0] == "@PITANJE", split[1].strip())

def validate_questionline(qline: str) -> Tuple[bool, str]:
    """
    Ensures the provided question line conforms to the form '??? <question>'.
    Returned tuple contains (validation result, question)
    """
    split = qline.split(" ")

    if len(split) == 1:
        return (False, "")
    else:
        return (split[0] == "???", " ".join(split[1:]))

def validate_zaokruzi_answer(answer: str) -> Tuple[bool, bool, str]:
    """
    Ensures the provided answer conforms to the form '@+/- <answer>'. Returned tuple contains
    (validation result, right/wrong, answer statement)
    """
    split = answer.split(" ")

    if len(split) == 1:
        return (False, "")
    else:
        valid_answer: bool = (split[0] == "@+" or split[0] == "@-")
        atype: bool = True if split[0] == "@+" else False
        astmt: str = " ".join(split[1:])
        
        return (valid_answer, atype, astmt)

def validate_dane_answer(answer: str) -> Tuple[bool, bool]:
    """
    Ensures the provided answer conforms to the form '@DA/NE'. Returned tuple contains
    (validation result, true/false)
    """
    answer = answer.strip()
    
    if answer == "@DA":
        return (True, True)
    elif answer == "@NE":
        return (True, False)
    else:
        return (False, False)

def validate_dopuni_answer(answer: str) -> Tuple[bool, str, str]:
    """
    Ensures the provided answer conforms to the form '@# <answer>'. Returned tuple contains
    (validation result, number, answer statement)
    """
    split = answer.split(" ")

    if len(split) == 1:
        return (False, "", "")
    else:
        valid_answer: bool = (split[0].startswith("@"))
        answerid: str = (split[0])[1:]
        astmt: str = " ".join(split[1:])

        return (valid_answer, answerid, astmt)